/** NO+ | Portada independiente y 36 noticias en 11 páginas interiores. */
export const PAGE_SECTIONS = Object.freeze([
 "Portada regional","Lambayeque: política local","Lambayeque: fiscalización y obras",
 "Lambayeque: sociedad, educación y seguridad","Lambayeque: economía y salud",
 "Perú: política nacional","Perú: justicia y economía","Perú: actualidad",
 "Internacional: geopolítica","Internacional: sociedad y economía",
 "Deportes: Lambayeque y Perú","Cultura, tecnología y servicios"
]);
export const PAGE_SLOT_COUNTS = Object.freeze([0,4,4,4,3,3,3,3,3,3,3,3]);
const hasText=x=>typeof x==="string"&&x.trim().length>0;
const date=x=>typeof x==="string"&&/^\d{4}-\d{2}-\d{2}$/.test(x)&&!Number.isNaN(Date.parse(x+"T00:00:00Z"));
const https=x=>{try{return typeof x==="string"&&new URL(x).protocol==="https:"}catch{return false}};
const slotId=(page,i)=>"P"+String(page).padStart(2,"0")+"-N"+(i+1);
export function createEditionDraft(editionDate){
 if(!date(editionDate))throw new TypeError("Fecha editorial inválida: YYYY-MM-DD");
 return {publication:"NO+",editionDate,status:"BORRADOR",autoPublish:false,
  pages:PAGE_SECTIONS.map((section,i)=>({page:i+1,section,
   slots:Array.from({length:PAGE_SLOT_COUNTS[i]},(_,j)=>({id:slotId(i+1,j),article:null}))}))};
}
/** Valida integridad formal. No verifica la veracidad ni crea un permiso de publicar. */
export function validateEdition(e){
 const issues=[];
 if(!e||typeof e!=="object")return {ready:false,count:0,issues:["Edición ausente"]};
 if(e.publication!=="NO+")issues.push("Marca inválida");
 if(!date(e.editionDate))issues.push("Fecha editorial inválida");
 if(e.autoPublish!==false)issues.push("autoPublish debe permanecer false");
 if(!Array.isArray(e.pages)||e.pages.length!==12)
  return {ready:false,count:0,issues:[...issues,"Se requieren exactamente 12 páginas"]};
 let count=0;const seen=new Set();
 e.pages.forEach((p,i)=>{
  const tag="Página "+(i+1);
  if(p?.page!==i+1||p?.section!==PAGE_SECTIONS[i])issues.push(tag+": orden o sección errónea");
  if(!Array.isArray(p?.slots)||p.slots.length!==PAGE_SLOT_COUNTS[i]){issues.push(tag+": se requieren "+PAGE_SLOT_COUNTS[i]+" espacios");return}
  p.slots.forEach((s,j)=>{
   const ref=tag+" noticia "+(j+1);
   if(s?.id!==slotId(i+1,j)||seen.has(s?.id))issues.push(ref+": ID incorrecto/repetido");
   seen.add(s?.id);
   const a=s?.article;
   if(!a||typeof a!=="object"){issues.push(ref+": noticia pendiente");return}
   count++;
   if(!hasText(a.title)||!hasText(a.body))issues.push(ref+": contenido incompleto");
   if(!date(a.eventDate)||!date(a.sourcePublicationDate))issues.push(ref+": fechas incompletas");
   if(!Array.isArray(a.sources)||!a.sources.length||!a.sources.every(src=>
      https(src?.url)&&hasText(src?.publisher)&&hasText(src?.checkedAt)))
    issues.push(ref+": fuentes sin URL HTTPS o trazabilidad");
   if(!hasText(a.verifiedBy))issues.push(ref+": falta revisión humana de fuentes");
   if(a.visual?.type!=="none"&&(!hasText(a.visual?.credit)||!hasText(a.visual?.rightsBasis)))
    issues.push(ref+": créditos o licencia de imagen pendientes");
   if(a.sensitiveAllegation===true&&(a.legalReviewed!==true||!hasText(a.replyStatus)))
    issues.push(ref+": falta revisión legal o registro de descargo");
   if(!hasText(a.approval?.editorId)||!hasText(a.approval?.approvedAt))
    issues.push(ref+": falta aprobación editorial");
  });
 });
 if(count!==36)issues.push("Se requieren 36 noticias (actual: "+count+")");
 return {ready:issues.length===0,count,issues};
}
