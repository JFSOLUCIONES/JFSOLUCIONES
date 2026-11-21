"""JF GeoPlan 360 v0.3.0 - isolated, authenticated reference API.

This module does NOT alter the Django-based Gestion360 site and uses a
local SQLite reference store; PostgreSQL/SSO integration requires staging.
No engineering documents are digitally signed by this service.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from io import BytesIO
import json
import os
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, field_validator
from .auth import Actor, require_role, scope_tenant, validate_actor
from .db import connect, initialize
from .geometry import analyze_polygon, export_dxf

UTC=timezone.utc
CATEGORIES={'vivienda','comercio','deportivo','infraestructura','inmobiliario','otro'}
DISCIPLINES={'architecture','structural','sanitary','electrical','geotechnical','topography'}

class ProjectIn(BaseModel):
    name: str = Field(min_length=3,max_length=160)
    category: str
    @field_validator('category')
    @classmethod
    def category_allowed(cls, v):
        if v not in CATEGORIES: raise ValueError('Categoría desconocida')
        return v

class SurveyIn(BaseModel):
    input_epsg: int
    vertices: list[list[float]] = Field(min_length=3,max_length=1000)

class VoucherIn(BaseModel):
    reference: str = Field(min_length=4,max_length=120)
    amount_pen: float = Field(ge=500,le=100000)

class ConfirmIn(BaseModel):
    voucher_id: str
    receipt_check_reference: str = Field(min_length=5,max_length=120)

class DeliverableIn(BaseModel):
    discipline: str
    file_sha256: str
    @field_validator('discipline')
    @classmethod
    def validate_discipline(cls,v):
        if v not in DISCIPLINES: raise ValueError('Especialidad desconocida')
        return v
    @field_validator('file_sha256')
    @classmethod
    def validate_hash(cls, v):
        if len(v)!=64 or any(ch not in '0123456789abcdef' for ch in v.lower()):
            raise ValueError('SHA256 inválido')
        return v.lower()

class ReviewIn(BaseModel):
    approved: bool
    checklist_completed: bool
    comment: str = Field(min_length=12,max_length=2500)


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def require_uuid(value: str) -> str:
    try: return str(uuid.UUID(value))
    except ValueError: raise HTTPException(status_code=404,detail='No encontrado') from None


def create_app(db_path: str, jwt_secret: str, issuer='jf-gestion360', audience='jf-geoplan360') -> FastAPI:
    if len(jwt_secret)<32: raise ValueError('Clave de verificación JWT de al menos 32 caracteres')
    if db_path == ':memory:': raise ValueError('Este prototipo requiere SQLite basado en archivo')
    initialize(db_path)
    app=FastAPI(title='JF GeoPlan 360 · API de laboratorio',version='0.3.0',docs_url='/docs')

    def actor(authorization: str | None = Header(default=None)) -> Actor:
        if not authorization or not authorization.startswith('Bearer '):
            raise HTTPException(status_code=401,detail='Acceso autenticado requerido')
        return validate_actor(authorization[7:],jwt_secret,issuer,audience)

    def audit(db, a:Actor,action:str,entity_type:str,entity_id:str|None=None, target_tenant:str|None=None):
        db.execute('INSERT INTO audit_logs(id,tenant_id,actor_id,action,entity_type,entity_id,occurred_at) VALUES (?,?,?,?,?,?,?)',
                   (str(uuid.uuid4()),target_tenant or a.tenant_id,a.sub,action,entity_type,entity_id,now_iso()))

    def active_subscription(db, a:Actor):
        if 'master' in a.roles: return
        sub=db.execute('SELECT expires_at FROM subscriptions WHERE tenant_id=?',(a.tenant_id,)).fetchone()
        if sub is None or datetime.fromisoformat(sub['expires_at'])<=datetime.now(UTC):
            raise HTTPException(status_code=402,detail='Suscripción vencida. Se permite consultar y registrar voucher, pero no operar.')

    def project_for_actor(db,pid:str,a:Actor):
        pid=require_uuid(pid)
        # Master can inspect all projects, with log before the response.
        if 'master' in a.roles:
            found=db.execute('SELECT * FROM projects WHERE id=?',(pid,)).fetchone()
        else:
            found=db.execute('SELECT * FROM projects WHERE id=? AND tenant_id=?',(pid,a.tenant_id)).fetchone()
        if not found: raise HTTPException(status_code=404,detail='Proyecto no encontrado')
        return found

    @app.get('/health')
    def health():
        return {'status':'ok','environment':'lab','engineering_signature':False,'production_ready':False}

    @app.get('/v1/tenants/{tenant_id}/subscription')
    def subscription(tenant_id: str,a:Actor=Depends(actor)):
        tid=scope_tenant(a,tenant_id)
        with connect(db_path) as db:
            s=db.execute('SELECT active_from,expires_at,amount_pen,duration_days FROM subscriptions WHERE tenant_id=?',(tid,)).fetchone()
        if not s: return {'active':False,'pending':True,'amount_pen':500,'duration_days':30}
        expires=datetime.fromisoformat(s['expires_at'])
        remains=(expires-datetime.now(UTC)).total_seconds()/86400
        return {'active':remains>0,'expires_at':s['expires_at'],'days_remaining':max(0,round(remains,2)),'renewal_notice':0<remains<=2,
                'amount_pen':s['amount_pen'],'duration_days':s['duration_days']}

    @app.post('/v1/tenants/{tenant_id}/vouchers',status_code=201)
    def submit_voucher(tenant_id:str,body:VoucherIn,a:Actor=Depends(actor)):
        tid=scope_tenant(a,tenant_id)
        voucher_id=str(uuid.uuid4())
        with connect(db_path) as db:
            db.execute('INSERT INTO vouchers(id,tenant_id,reference,amount_pen,created_by,created_at) VALUES (?,?,?,?,?,?)',
                       (voucher_id,tid,body.reference,body.amount_pen,a.sub,now_iso()))
            audit(db,a,'voucher_submitted','voucher',voucher_id)
        return {'id':voucher_id,'state':'pending_manual_check','nota':'No demuestra recepción de pago'}

    @app.post('/v1/tenants/{tenant_id}/subscription/confirm')
    def confirm_subscription(tenant_id:str,body:ConfirmIn,a:Actor=Depends(actor)):
        require_role(a,'master')
        tid=scope_tenant(a,tenant_id)
        voucher_id=require_uuid(body.voucher_id)
        with connect(db_path) as db:
            v=db.execute('SELECT * FROM vouchers WHERE id=? AND tenant_id=?',(voucher_id,tid)).fetchone()
            if not v: raise HTTPException(404,'Voucher inexistente')
            if v['state']!='pending_manual_check': raise HTTPException(409,'Voucher ya procesado')
            if v['amount_pen']<500: raise HTTPException(422,'Pago insuficiente')
            previous=db.execute('SELECT expires_at FROM subscriptions WHERE tenant_id=?',(tid,)).fetchone()
            now=datetime.now(UTC)
            start=max(now,datetime.fromisoformat(previous['expires_at'])) if previous else now
            expires=start+timedelta(days=30)
            db.execute('INSERT INTO subscriptions(tenant_id,active_from,expires_at,amount_pen,duration_days,receipt_reference,activated_by) VALUES (?,?,?,?,?,?,?) ON CONFLICT(tenant_id) DO UPDATE SET active_from=excluded.active_from,expires_at=excluded.expires_at,receipt_reference=excluded.receipt_reference,activated_by=excluded.activated_by',
                      (tid,start.isoformat(),expires.isoformat(),500,30,body.receipt_check_reference,a.sub))
            db.execute("UPDATE vouchers SET state='verified_by_master' WHERE id=? AND tenant_id=?",(voucher_id,tid))
            audit(db,a,'subscription_manual_confirm','subscription',tid)
        return {'active':True,'expires_at':expires.isoformat(),'verified_manually':True,'payment_gateway':False}

    @app.post('/v1/projects',status_code=201)
    def create_project(body:ProjectIn,a:Actor=Depends(actor)):
        require_role(a,'master','tenant_admin','operator','engineer','architect')
        project_id=str(uuid.uuid4())
        with connect(db_path) as db:
            active_subscription(db,a)
            db.execute('INSERT INTO projects VALUES (?,?,?,?,?,?)',
                       (project_id,a.tenant_id,body.name,body.category,a.sub,now_iso()))
            audit(db,a,'project_created','project',project_id)
        return {'id':project_id,'tenant_id':a.tenant_id,'name':body.name,'category':body.category}

    @app.get('/v1/projects')
    def list_projects(a:Actor=Depends(actor)):
        with connect(db_path) as db:
            rows=db.execute('SELECT id,tenant_id,name,category,created_at FROM projects WHERE tenant_id=? ORDER BY created_at DESC',(a.tenant_id,)).fetchall()
        return {'projects':[dict(row) for row in rows]}

    @app.get('/v1/projects/{project_id}')
    def get_project(project_id:str,a:Actor=Depends(actor)):
        with connect(db_path) as db:
            project=project_for_actor(db,project_id,a)
            audit(db,a,'project_viewed','project',project_id,project['tenant_id'])
        return dict(project)

    @app.post('/v1/projects/{project_id}/surveys',status_code=201)
    def create_survey(project_id:str,body:SurveyIn,a:Actor=Depends(actor)):
        require_role(a,'master','tenant_admin','operator','engineer','architect')
        try: geo=analyze_polygon(body.vertices,body.input_epsg)
        except ValueError as exc: raise HTTPException(422,detail=str(exc)) from None
        survey_id=str(uuid.uuid4())
        with connect(db_path) as db:
            active_subscription(db,a)
            p=project_for_actor(db,project_id,a)
            db.execute('INSERT INTO surveys VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (survey_id,p['id'],p['tenant_id'],body.input_epsg,geo.projected_epsg,
                 json.dumps(body.vertices),json.dumps(geo.projected_vertices),geo.area_m2,geo.perimeter_m,a.sub,now_iso()))
            audit(db,a,'survey_created','survey',survey_id,p['tenant_id'])
        return {'id':survey_id,'source_epsg':geo.source_epsg,'projected_epsg':geo.projected_epsg,
                'area_m2':geo.area_m2,'perimeter_m':geo.perimeter_m,'professional_validation_required':True}

    @app.get('/v1/projects/{project_id}/surveys/{survey_id}/dxf',response_class=PlainTextResponse)
    def download_dxf(project_id:str,survey_id:str,a:Actor=Depends(actor)):
        sid=require_uuid(survey_id)
        with connect(db_path) as db:
            p=project_for_actor(db,project_id,a)
            s=db.execute('SELECT * FROM surveys WHERE id=? AND project_id=? AND tenant_id=?',
                         (sid,p['id'],p['tenant_id'])).fetchone()
            if not s: raise HTTPException(404,'Levantamiento no encontrado')
            audit(db,a,'dxf_downloaded','survey',sid,p['tenant_id'])
        dxf=export_dxf(tuple(tuple(row) for row in json.loads(s['projected_vertices_json'])),s['projected_epsg'])
        return PlainTextResponse(dxf,media_type='application/dxf',headers={'Content-Disposition':f'attachment; filename="geoplan-{sid}.dxf"'})

    @app.post('/v1/projects/{project_id}/deliverables',status_code=201)
    def create_deliverable(project_id:str,body:DeliverableIn,a:Actor=Depends(actor)):
        require_role(a,'master','tenant_admin','operator','engineer','architect')
        did=str(uuid.uuid4())
        with connect(db_path) as db:
            active_subscription(db,a)
            p=project_for_actor(db,project_id,a)
            db.execute('INSERT INTO deliverables(id,project_id,tenant_id,discipline,file_sha256,author_id,created_at) VALUES (?,?,?,?,?,?,?)',
                (did,p['id'],p['tenant_id'],body.discipline,body.file_sha256,a.sub,now_iso()))
            audit(db,a,'deliverable_created','deliverable',did,p['tenant_id'])
        return {'id':did,'status':'draft','signed':False}

    @app.post('/v1/projects/{project_id}/deliverables/{deliverable_id}/submit')
    def submit_deliverable(project_id:str,deliverable_id:str,a:Actor=Depends(actor)):
        require_role(a,'master','tenant_admin','operator','engineer','architect')
        did=require_uuid(deliverable_id)
        with connect(db_path) as db:
            active_subscription(db,a)
            p=project_for_actor(db,project_id,a)
            d=db.execute('SELECT * FROM deliverables WHERE id=? AND project_id=? AND tenant_id=?',(did,p['id'],p['tenant_id'])).fetchone()
            if not d: raise HTTPException(404,'No encontrado')
            if d['status'] not in ('draft','changes_requested'): raise HTTPException(409,'Estado inválido')
            db.execute("UPDATE deliverables SET status='submitted' WHERE id=?",(did,))
            audit(db,a,'submitted_for_professional_review','deliverable',did,p['tenant_id'])
        return {'status':'submitted','signed':False}

    @app.post('/v1/projects/{project_id}/deliverables/{deliverable_id}/review')
    def professional_review(project_id:str,deliverable_id:str,body:ReviewIn,a:Actor=Depends(actor)):
        require_role(a,'engineer','architect')
        if not a.professional_verified:
            raise HTTPException(403,'Verificación profesional pendiente')
        did=require_uuid(deliverable_id)
        with connect(db_path) as db:
            active_subscription(db,a)
            p=project_for_actor(db,project_id,a)
            d=db.execute('SELECT * FROM deliverables WHERE id=? AND project_id=? AND tenant_id=?',(did,p['id'],p['tenant_id'])).fetchone()
            if not d: raise HTTPException(404,'No encontrado')
            if d['status']!='submitted': raise HTTPException(409,'El plano no está presentado para revisión')
            if d['author_id']==a.sub: raise HTTPException(403,'Revisión independiente requerida')
            if d['discipline']=='architecture' and ('architect' not in a.roles or a.profession!='architect'):
                raise HTTPException(403,'Arquitectura requiere arquitecto habilitado')
            if d['discipline']=='structural' and ('engineer' not in a.roles or a.profession!='civil_engineer'):
                raise HTTPException(403,'Estructuras requiere ingeniero civil habilitado')
            if d['discipline'] in ('sanitary','electrical','geotechnical','topography') and a.profession not in ('civil_engineer','sanitary_engineer','electrical_engineer','geotechnical_engineer','surveyor'):
                raise HTTPException(403,'Especialista requerido')
            if body.approved and not body.checklist_completed:
                raise HTTPException(422,'Checklist técnico obligatorio')
            state='approved_for_signature' if body.approved else 'changes_requested'
            db.execute('UPDATE deliverables SET status=?,reviewer_id=?,review_comment=?,reviewed_at=? WHERE id=?',
                       (state,a.sub,body.comment,now_iso(),did))
            audit(db,a,'professional_review_'+state,'deliverable',did,p['tenant_id'])
        return {'status':state,'signed':False,'note':'La firma profesional o digital se tramita externamente tras validar identidad y responsabilidad'}

    return app


def from_env():
    secret=os.environ.get('GEOPLAN_JWT_SECRET','')
    db=os.environ.get('GEOPLAN_DB_PATH','')
    if not db: raise RuntimeError('Configurar GEOPLAN_DB_PATH explícitamente')
    if len(secret)<32: raise RuntimeError('Configurar GEOPLAN_JWT_SECRET, al menos 32 caracteres')
    return create_app(db,secret)
