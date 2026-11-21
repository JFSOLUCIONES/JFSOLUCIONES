/** JF GeoPlan 360 · matemáticas de gabinete. Sin validez catastral. */
export const DEMO_VARIANTS = Object.freeze({
  f6: { label: 'Fútbol 6', width: 25, length: 40, investment: 759541, minPlotWidth: 80, minPlotLength: 60 },
  f7: { label: 'Fútbol 7', width: 30, length: 50, investment: 1013512, minPlotWidth: 80, minPlotLength: 80 },
});
const finitePositive = (x) => Number.isFinite(x) && x > 0;
export function layoutTwoPitches(plotWidth, plotLength, variant='f6', safety=2, edge=2, front=12) {
  const choice=DEMO_VARIANTS[variant];
  if(!choice || ![plotWidth,plotLength,safety,edge,front].every(Number.isFinite) || !finitePositive(plotWidth) || !finitePositive(plotLength) || safety<0 || edge<0 || front<0) throw new RangeError('Parámetros geométricos inválidos');
  const requiredWidth=2*(choice.width+2*safety)+2*edge;
  const requiredLength=choice.length+2*safety+2*edge+front;
  const fits=plotWidth>=requiredWidth && plotLength>=requiredLength;
  const x1=edge+safety,y=front+edge+safety;
  const x2=x1+choice.width+2*safety;
  const pitches=fits ? [{x:x1,y,width:choice.width,length:choice.length},{x:x2,y,width:choice.width,length:choice.length}]:[];
  return {fits,plotArea:plotWidth*plotLength,playingArea:2*choice.width*choice.length,requiredWidth,requiredLength,frontServicesArea:plotWidth*front,remainingArea:plotWidth*plotLength-2*choice.width*choice.length, pitches, label:choice.label, investment:choice.investment};
}
export function finance({hourlyRate=75,hoursPerPitch=5,days=28,monthlyRent=4000,monthlyOtherCosts=11200,barContribution=3600,investment=759541}={}) {
  const values={hourlyRate,hoursPerPitch,days,monthlyRent,monthlyOtherCosts,barContribution,investment};
  if(Object.values(values).some(v=>!Number.isFinite(v)||v<0)) throw new RangeError('Variables financieras inválidas');
  if(days>31 || hoursPerPitch>24) throw new RangeError('Jornada inválida');
  const revenue=2*hourlyRate*hoursPerPitch*days;
  const cashflow=revenue+barContribution-monthlyRent-monthlyOtherCosts;
  return {revenue,cashflow,annualCashflow:cashflow*12,payback:cashflow>0?investment/(12*cashflow):null};
}
export function parsePlanarPoints(raw) {
  if(typeof raw!=='string') throw new TypeError('Texto no válido');
  const points=[];
  for(const [index,line] of raw.split(/\r?\n/).entries()){
    const value=line.trim(); if(!value || value.startsWith('#')) continue;
    const parts=value.split(/[;,\t]/).map(t=>t.trim());
    if(parts.length!==2 && parts.length!==3) throw new Error(`Línea ${index+1}: formato X,Y o NOMBRE,X,Y`);
    const x=Number(parts.at(-2)),y=Number(parts.at(-1));
    if(!Number.isFinite(x)||!Number.isFinite(y)) throw new Error(`Línea ${index+1}: coordenadas inválidas`);
    points.push({name:parts.length===3?parts[0]:`P${points.length+1}`,x,y});
  }
  if(points.length<3) throw new Error('Se necesitan al menos tres vértices');
  if(points.length>10000) throw new Error('Demasiados vértices');
  return points;
}
export function calculatePlanarPolygon(points){
  if(!Array.isArray(points)||points.length<3) throw new Error('Polígono incompleto');
  const x0=points[0].x,y0=points[0].y;
  let doubleArea=0,perimeter=0;
  for(let i=0;i<points.length;i++){
    const a=points[i],b=points[(i+1)%points.length];
    if(![a.x,a.y,b.x,b.y].every(Number.isFinite)) throw new RangeError('Coordenadas inválidas');
    doubleArea+=(a.x-x0)*(b.y-y0)-(b.x-x0)*(a.y-y0);
    perimeter+=Math.hypot(b.x-a.x,b.y-a.y);
  }
  const area=Math.abs(doubleArea)/2;
  if(area<=1e-8) throw new Error('Polígono degenerado');
  return {area,perimeter,points:points.length};
}
export function exportDXFR12(points){
  calculatePlanarPolygon(points);
  // DXF ASCII R12 básico, entidades LINE. NO georreferencia ni valida topología.
  const lines=['0','SECTION','2','HEADER','9','$ACADVER','1','AC1009','0','ENDSEC','0','SECTION','2','ENTITIES'];
  for(let i=0;i<points.length;i++){
    const p=points[i],q=points[(i+1)%points.length];
    lines.push('0','LINE','8','LOTE_CONCEPTUAL','10',String(p.x),'20',String(p.y),'30','0','11',String(q.x),'21',String(q.y),'31','0');
  }
  lines.push('0','ENDSEC','0','EOF'); return lines.join('\n')+'\n';
}
export function safeCatalogUrl(value){
  if(typeof value!=='string') return null;
  try{const u=new URL(value);if(u.protocol!=='https:'||u.username||u.password||u.search||u.hash)return null; if(/\s/.test(value))return null;return u.href;}catch{return null;}
}
