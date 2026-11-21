from datetime import datetime, timedelta, timezone
from pathlib import Path
import hashlib
import uuid
import jwt
import pytest
from fastapi.testclient import TestClient
from geoplan_api.main import create_app
from geoplan_api.geometry import analyze_polygon

SECRET='f'*64
TENANT_A='11111111-1111-4111-8111-111111111111'
TENANT_B='22222222-2222-4222-8222-222222222222'
MASTER_TENANT='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'
RECT=[[630000,9250000],[630040,9250000],[630040,9250025],[630000,9250025]]


def token(sub,tenant=TENANT_A,roles=('operator',),verified=False,profession=None,secret=SECRET,expires=3600):
    payload={'sub':sub,'tenant_id':tenant,'roles':list(roles),'iss':'jf-gestion360','aud':'jf-geoplan360',
             'professional_verified':verified,'profession':profession,'exp':datetime.now(timezone.utc)+timedelta(seconds=expires)}
    return jwt.encode(payload,secret,algorithm='HS256')

def h(sub='operator',tenant=TENANT_A,roles=('operator',),**kwargs):
    return {'Authorization':'Bearer '+token(sub,tenant,roles,**kwargs)}

@pytest.fixture
def setup(tmp_path):
    db=str(tmp_path/'geoplan.sqlite3')
    app=create_app(db,SECRET)
    return TestClient(app),db


def activate(client,tenant=TENANT_A):
    v=client.post(f'/v1/tenants/{tenant}/vouchers',json={'reference':'bank-verified-reference','amount_pen':500},headers=h()).json()
    r=client.post(f'/v1/tenants/{tenant}/subscription/confirm',json={'voucher_id':v['id'],'receipt_check_reference':'bank_statement_checked'},
                  headers=h('master',MASTER_TENANT,('master',)))
    assert r.status_code==200,r.text
    return v['id']


def project(client,name='Campo deportivo Ferreñafe'):
    r=client.post('/v1/projects',headers=h(),json={'name':name,'category':'deportivo'})
    assert r.status_code==201,r.text
    return r.json()['id']


def survey(client,pid):
    r=client.post(f'/v1/projects/{pid}/surveys',headers=h(),json={'input_epsg':32717,'vertices':RECT})
    assert r.status_code==201,r.text
    return r


def test_health_and_no_default_secrets(setup):
    c,_=setup
    assert c.get('/health').json()['production_ready'] is False
    assert c.get('/v1/projects').status_code==401
    with pytest.raises(ValueError): create_app('/tmp/should-not-be-created.sqlite3','short')


def test_voucher_requires_master_validation(setup):
    c,_=setup
    before=c.post('/v1/projects',headers=h(),json={'name':'Proyecto inicial','category':'vivienda'})
    assert before.status_code==402
    v=c.post(f'/v1/tenants/{TENANT_A}/vouchers',headers=h(),json={'reference':'Voucher-001','amount_pen':500})
    assert v.status_code==201 and v.json()['state']=='pending_manual_check'
    bid=v.json()['id']
    assert c.post(f'/v1/tenants/{TENANT_A}/subscription/confirm',headers=h(),json={'voucher_id':bid,'receipt_check_reference':'bank_statement_checked'}).status_code==403
    assert c.post(f'/v1/tenants/{TENANT_A}/subscription/confirm',headers=h('master',MASTER_TENANT,('master',)),json={'voucher_id':bid,'receipt_check_reference':'bank_statement_checked'}).status_code==200
    assert c.post(f'/v1/tenants/{TENANT_A}/subscription/confirm',headers=h('master',MASTER_TENANT,('master',)),json={'voucher_id':bid,'receipt_check_reference':'bank_statement_checked'}).status_code==409
    assert c.get(f'/v1/tenants/{TENANT_A}/subscription',headers=h()).json()['active'] is True


def test_cross_tenant_access_blocked_for_client(setup):
    c,_=setup;activate(c);pid=project(c)
    assert len(c.get('/v1/projects',headers=h('other',TENANT_B)).json()['projects'])==0
    assert c.get(f'/v1/projects/{pid}',headers=h('other',TENANT_B)).status_code==404
    assert c.get(f'/v1/projects/{pid}',headers=h('master',MASTER_TENANT,('master',))).status_code==200
    assert c.get(f'/v1/tenants/{TENANT_A}/subscription',headers=h('other',TENANT_B)).status_code==404


def test_planar_m2_perimeter(setup):
    c,_=setup;activate(c);pid=project(c)
    res=survey(c,pid).json()
    assert res['area_m2']==1000.0
    assert res['perimeter_m']==130.0
    assert res['projected_epsg']==32717
    dxf=c.get(f'/v1/projects/{pid}/surveys/{res["id"]}/dxf',headers=h())
    assert dxf.status_code==200 and 'LOTE_CONCEPTUAL' in dxf.text
    assert c.get(f'/v1/projects/{pid}/surveys/{res["id"]}/dxf',headers=h('other',TENANT_B)).status_code==404


def test_geographic_auto_utm_and_invalid_polygon():
    g=analyze_polygon([[-79.8,-6.6],[-79.7999,-6.6],[-79.7999,-6.5999],[-79.8,-6.5999]],4326)
    assert g.projected_epsg==32717 and 10<g.area_m2<500
    with pytest.raises(ValueError): analyze_polygon([[0,0],[10,10],[0,10],[10,0]],32717)
    with pytest.raises(ValueError): analyze_polygon(RECT,4326)
    with pytest.raises(ValueError): analyze_polygon(RECT,999999)


def test_jwt_authentication_fail_closed(setup):
    c,_=setup
    assert c.get('/v1/projects',headers={'Authorization':'Bearer '+token('bad',secret='x'*64)}).status_code==401
    assert c.get('/v1/projects',headers={'Authorization':'Bearer '+token('expired',expires=-60)}).status_code==401
    assert c.get('/v1/projects',headers={'Authorization':'Bearer invalid'}).status_code==401


def test_professional_review_cannot_be_rubber_stamp(setup):
    c,_=setup;activate(c);pid=project(c)
    sha=hashlib.sha256(b'draft only').hexdigest()
    d=c.post(f'/v1/projects/{pid}/deliverables',headers=h(),json={'discipline':'structural','file_sha256':sha})
    assert d.status_code==201
    did=d.json()['id']
    url=f'/v1/projects/{pid}/deliverables/{did}'
    assert c.post(url+'/submit',headers=h()).status_code==200
    review={'approved':True,'checklist_completed':True,'comment':'Se verificaron estructuras y observaciones del expediente presentado.'}
    assert c.post(url+'/review',headers=h('operator'),json=review).status_code==403
    assert c.post(url+'/review',headers=h('reviewer',roles=('engineer',),verified=False,profession='civil_engineer'),json=review).status_code==403
    assert c.post(url+'/review',headers=h('reviewer',roles=('architect',),verified=True,profession='architect'),json=review).status_code==403
    assert c.post(url+'/review',headers=h('reviewer',roles=('engineer',),verified=True,profession='civil_engineer'),json={**review,'checklist_completed':False}).status_code==422
    approved=c.post(url+'/review',headers=h('reviewer',roles=('engineer',),verified=True,profession='civil_engineer'),json=review)
    assert approved.status_code==200 and approved.json()=={
      'status':'approved_for_signature','signed':False,'note':'La firma profesional o digital se tramita externamente tras validar identidad y responsabilidad'}
    assert c.post(url+'/review',headers=h('reviewer',roles=('engineer',),verified=True,profession='civil_engineer'),json=review).status_code==409


def test_reviewer_cannot_approve_own_draft(setup):
    c,_=setup;activate(c);pid=project(c)
    author=h('same',roles=('engineer',),verified=True,profession='civil_engineer')
    sha='a'*64
    d=c.post(f'/v1/projects/{pid}/deliverables',headers=author,json={'discipline':'structural','file_sha256':sha}).json()['id']
    c.post(f'/v1/projects/{pid}/deliverables/{d}/submit',headers=author)
    r=c.post(f'/v1/projects/{pid}/deliverables/{d}/review',headers=author,json={'approved':True,'checklist_completed':True,'comment':'Revisión personal que debe ser denegada'})
    assert r.status_code==403


def test_expired_subscription_allows_read_and_voucher(setup):
    import sqlite3
    c,db=setup;activate(c);pid=project(c);sid=survey(c,pid).json()['id']
    with sqlite3.connect(db) as con:
        con.execute('UPDATE subscriptions SET expires_at=? WHERE tenant_id=?',((datetime.now(timezone.utc)-timedelta(hours=1)).isoformat(),TENANT_A))
    assert c.post('/v1/projects',headers=h(),json={'name':'No permitido','category':'deportivo'}).status_code==402
    assert c.get(f'/v1/projects/{pid}/surveys/{sid}/dxf',headers=h()).status_code==200
    assert c.post(f'/v1/tenants/{TENANT_A}/vouchers',headers=h(),json={'reference':'voucher-renew','amount_pen':500}).status_code==201


def test_no_cross_tenant_survey_injection(setup):
    c,_=setup;activate(c);pid=project(c)
    r=c.post(f'/v1/projects/{pid}/surveys',headers=h('other',TENANT_B,('operator',)),json={'input_epsg':32717,'vertices':RECT})
    assert r.status_code in (402,404)
    c2=c.post('/v1/projects',headers=h('viewer',TENANT_A,('client',)),json={'name':'No permitido','category':'vivienda'})
    assert c2.status_code==403
