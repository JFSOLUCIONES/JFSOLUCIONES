"""JWT validation delegated to a trusted issuer. Never issue tokens to clients from this service."""
from dataclasses import dataclass
import uuid
import jwt
from fastapi import HTTPException, status

@dataclass(frozen=True)
class Actor:
    sub: str
    tenant_id: str
    roles: frozenset[str]
    professional_verified: bool = False
    profession: str | None = None


def validate_actor(raw_token: str, secret: str, issuer: str, audience: str) -> Actor:
    if not raw_token or not secret or len(secret)<32:
        raise HTTPException(status_code=401, detail='Autenticación no disponible')
    try:
        claims=jwt.decode(raw_token, secret, algorithms=['HS256'],
                          issuer=issuer, audience=audience, options={'require':['exp','iss','aud','sub','tenant_id']},leeway=10)
        tenant_id = str(uuid.UUID(str(claims['tenant_id'])))
        sub = str(claims['sub'])
        if len(sub)>128 or not sub:
            raise ValueError('sub')
        roles = frozenset(claims.get('roles', []))
        if roles - {'master','tenant_admin','engineer','architect','operator','client'}:
            raise ValueError('unknown role')
        return Actor(sub,tenant_id,roles,claims.get('professional_verified') is True, claims.get('profession'))
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise HTTPException(status_code=401,detail='Token no válido') from None


def require_role(actor: Actor, *allowed):
    if actor.roles.isdisjoint(set(allowed)):
        raise HTTPException(status_code=403,detail='Permiso insuficiente')


def scope_tenant(actor: Actor, tenant_id: str):
    try:
        tid = str(uuid.UUID(tenant_id))
    except ValueError:
        raise HTTPException(status_code=404,detail='No encontrado') from None
    if tid != actor.tenant_id and 'master' not in actor.roles:
        raise HTTPException(status_code=404,detail='No encontrado')
    return tid
