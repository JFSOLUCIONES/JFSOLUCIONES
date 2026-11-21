import test from 'node:test';
import assert from 'node:assert/strict';
import {normaliseLink,linksForActor,catalogSummary} from './registry.mjs';
const assets=[
{systemId:'geo',enterpriseEnabled:true,masterUrl:'https://gestion360.jfconnect.online/admin/',masterApproved:true,operativeUrl:'https://n8n.jfconnect.online/',operativeApproved:true,clientEnabled:true,clientApproved:true,clientUrl:'https://portal-ejemplo.test/cliente',tenantId:'tenant-a'},
{systemId:'sports',enterpriseEnabled:true,masterUrl:'https://gestion360.jfconnect.online/admin/sports/',masterApproved:true,clientEnabled:true,clientApproved:true,clientUrl:'https://portal-ejemplo.test/sports',tenantId:'tenant-b'}
];
test('URL HTTPS valida',()=>assert.equal(normaliseLink('https://gestion360.jfconnect.online/admin/'),'https://gestion360.jfconnect.online/admin/'));
test('URL bloquea contraseñas, consultas y protocolos inseguros',()=>{for(const x of ['http://a.example','ftp://b.example','https://u:p@example.com','https://test.com/?token=secret','javascript:alert(1)','pendiente']) assert.equal(normaliseLink(x),null);});
test('MASTER autorizado ve enlaces internos publicados',()=>{const x=linksForActor({authenticated:true,id:'a',role:'master',enterpriseApproved:true},assets);assert.equal(x.length,3);assert.ok(x.every(a=>a.kind!=='client'));});
test('Cliente ve solamente su tenant',()=>{const x=linksForActor({authenticated:true,id:'u',role:'client',tenantId:'tenant-a'},assets);assert.equal(x.length,1);assert.equal(x[0].systemId,'geo');assert.equal(x[0].kind,'client');});
test('Cliente sin tenant no ve enlaces',()=>assert.deepEqual(linksForActor({authenticated:true,id:'u',role:'client'},assets),[]));
test('Sucesor sin activación legal no ve enlaces',()=>assert.deepEqual(linksForActor({authenticated:true,id:'h',role:'successor',enterpriseApproved:true,legalActivationApproved:false},assets),[]));
test('Usuario no autenticado no ve enlaces',()=>assert.deepEqual(linksForActor({authenticated:false,id:'u',role:'master',enterpriseApproved:true},assets),[]));
test('Registro no aprobado o inactivo permanece oculto',()=>{const x=linksForActor({authenticated:true,id:'u',role:'client',tenantId:'tenant-a'},[{...assets[0],clientApproved:false}]);assert.deepEqual(x,[])});
test('Resumen cuenta solo URLs sintácticamente válidas',()=>{const r=catalogSummary(assets);assert.equal(r.assets,2);assert.equal(r.syntacticallyValid.master,2);assert.equal(r.syntacticallyValid.client,2)});
