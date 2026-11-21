/**
 * Geometría conceptual sin coordenadas catastrales ni validez constructiva.
 * Ejes relativos del supuesto lote rectangular, en metros.
 */
export function layoutTwoPitches({ plotWidth, plotHeight, pitchWidth, pitchHeight, safety = 2, edge = 2 } = {}) {
  const nums = { plotWidth, plotHeight, pitchWidth, pitchHeight, safety, edge };
  for (const [key,value] of Object.entries(nums)) {
    if (typeof value !== "number" || !Number.isFinite(value) || value < 0) throw new TypeError(`Medida inválida: ${key}`);
  }
  if (pitchWidth === 0 || pitchHeight === 0 || plotWidth === 0 || plotHeight === 0) throw new TypeError("Las dimensiones deben ser positivas");
  const fullW = pitchWidth + 2*safety, fullH = pitchHeight + 2*safety;
  const requiredW = fullW + 2*edge;
  const requiredH = 2*fullH + 2*edge;
  if (plotWidth < requiredW || plotHeight < requiredH) {
    return { fits: false, reason:"El rectángulo simulado no admite dos campos con estas bandas", requiredWidth:requiredW,requiredHeight:requiredH, area:plotWidth*plotHeight };
  }
  const x = plotWidth - edge - safety - pitchWidth;
  const firstY = edge + safety;
  return {
    fits: true,
    reference:"Diseño de gabinete, no georreferenciado; verificar topografía y normativa",
    plot:{ width:plotWidth,height:plotHeight,area:plotWidth*plotHeight },
    pitches:[0,1].map(i=>({ id:i+1, x, y:firstY+i*fullH, width:pitchWidth,height:pitchHeight, playingArea:pitchWidth*pitchHeight })),
    safety,
    leftSideStripWidth: x-safety-edge,
    retainedServicesAreaIsUnverified:true
  };
}
