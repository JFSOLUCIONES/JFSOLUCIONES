/**
 * Implantación conceptual: 2 canchas contiguas y una franja frontal para servicios.
 * Coordenadas relativas y medidas hipotéticas, NO levantamiento topográfico.
 * pitchWidth = dimensión transversal; pitchHeight = dimensión longitudinal.
 */
export function layoutTwoPitches({plotWidth,plotHeight,pitchWidth,pitchHeight,safety=2,edge=2,frontServicesDepth=12}={}) {
  const dims={plotWidth,plotHeight,pitchWidth,pitchHeight,safety,edge,frontServicesDepth};
  for(const [key,value] of Object.entries(dims)){
    if(typeof value !== "number"||!Number.isFinite(value)||value<0) throw new TypeError(`Medida inválida: ${key}`);
  }
  if(!plotWidth||!plotHeight||!pitchWidth||!pitchHeight) throw new TypeError("Las dimensiones deben ser positivas");
  const requiredWidth=2*(pitchWidth+2*safety)+2*edge;
  const requiredHeight=pitchHeight+2*safety+2*edge+frontServicesDepth;
  if(plotWidth<requiredWidth||plotHeight<requiredHeight){
    return {fits:false,reason:"Área insuficiente para dos canchas y franja frontal",requiredWidth,requiredHeight,plotAreaM2:plotWidth*plotHeight};
  }
  const initialX=edge+safety;
  const y=frontServicesDepth+edge+safety;
  const pitches=[0,1].map(i=>({
    id:i+1,x:initialX+i*(pitchWidth+2*safety),y,width:pitchWidth,height:pitchHeight,playingAreaM2:pitchWidth*pitchHeight
  }));
  return {fits:true,assumptions:"Plano conceptual sin georreferenciación, pendiente de accesos/drenaje/normativa",plot:{width:plotWidth,height:plotHeight,areaM2:plotWidth*plotHeight},pitches,safety,edge,frontServicesDepth,residualWidthM:plotWidth-(initialX+(pitchWidth+2*safety)+pitchWidth+edge+safety)};
}