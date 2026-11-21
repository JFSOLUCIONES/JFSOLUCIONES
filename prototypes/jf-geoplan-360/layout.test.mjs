import test from 'node:test';
import assert from 'node:assert/strict';
import { layoutTwoPitches } from './layout.mjs';

test('fútbol 6 supuesto 80 x 60 encaja sin salir del lote', () => {
 const r=layoutTwoPitches({plotWidth:80,plotHeight:60,pitchWidth:40,pitchHeight:25});
 assert.equal(r.fits,true); assert.equal(r.pitches.length,2);
 for(const p of r.pitches){ assert.ok(p.x>=2); assert.ok(p.y>=2); assert.ok(p.x+p.width<=78); assert.ok(p.y+p.height<=58); }
 assert.equal(r.plot.area,4800);
});
test('fútbol 7 supuesto 80 x 80 encaja',()=>{
 const r=layoutTwoPitches({plotWidth:80,plotHeight:80,pitchWidth:50,pitchHeight:30});
 assert.equal(r.fits,true); assert.equal(r.plot.area,6400);
});
test('rechaza lote insuficiente',()=>{
 const r=layoutTwoPitches({plotWidth:30,plotHeight:40,pitchWidth:40,pitchHeight:25}); assert.equal(r.fits,false);
});
test('rechaza mediciones no válidas',()=>{
 assert.throws(()=>layoutTwoPitches({plotWidth:80,plotHeight:-1,pitchWidth:40,pitchHeight:25}),TypeError);
});
