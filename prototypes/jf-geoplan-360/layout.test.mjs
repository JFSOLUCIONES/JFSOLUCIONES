import test from 'node:test';
import assert from 'node:assert/strict';
import { layoutTwoPitches } from './layout.mjs';

for(const cfg of [
 {plotWidth:80,plotHeight:60,pitchWidth:25,pitchHeight:40,expectedArea:4800},
 {plotWidth:80,plotHeight:80,pitchWidth:30,pitchHeight:50,expectedArea:6400},
]) {
 test(`encaje conceptual lateral ${cfg.plotWidth} x ${cfg.plotHeight}`,()=>{
  const r=layoutTwoPitches(cfg);
  assert.equal(r.fits,true); assert.equal(r.pitches.length,2);
  assert.equal(r.plot.areaM2,cfg.expectedArea);
  for(const p of r.pitches){assert.ok(p.x>=4);assert.ok(p.y>=16);assert.ok(p.x+p.width<=cfg.plotWidth-4);assert.ok(p.y+p.height<=cfg.plotHeight-4);}
  assert.ok(r.pitches[0].x+r.pitches[0].width<r.pitches[1].x);
 });
}
test('rechaza lote insuficiente',()=>{assert.equal(layoutTwoPitches({plotWidth:40,plotHeight:60,pitchWidth:25,pitchHeight:40}).fits,false)});
test('rechaza dimensiones negativas',()=>{assert.throws(()=>layoutTwoPitches({plotWidth:-1,plotHeight:60,pitchWidth:25,pitchHeight:40}),TypeError)});
