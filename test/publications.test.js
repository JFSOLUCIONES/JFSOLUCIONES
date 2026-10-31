import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
test('lote de nueve borradores supera control de calidad inicial',()=>{
 const out=execFileSync(process.execPath,['src/editorial/validate-posts.js','editorial/2026-10-31/9-publicaciones.json'],{encoding:'utf8'});
 const r=JSON.parse(out);
 assert.equal(r.posts,9);
 assert.equal(r.passed,true);
});
