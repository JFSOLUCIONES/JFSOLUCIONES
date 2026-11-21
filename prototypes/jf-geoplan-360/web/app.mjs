import { DEMO_VARIANTS, layoutTwoPitches, finance, parsePlanarPoints, calculatePlanarPolygon, exportDXFR12, safeCatalogUrl } from './logic.mjs';
const $=(id)=>document.getElementById(id);
const fmt=(v)=>new Intl.NumberFormat('es-PE',{maximumFractionDigits:1}).format(v);
const money=(v)=>'S/ '+new Intl.NumberFormat('es-PE',{maximumFractionDigits:0}).format(v);
let active='inicio';
const OPEN_LINKS=[
  {name:'JF Gestión360 · Administrador',description:'Entrada MASTER de la plataforma, requiere autenticación',url:'https://gestion360.jfconnect.online/admin/'},
  {name:'JF GeoPlan 360 · Ficha',description:'Ruta actualmente existente; aún muestra estado en desarrollo',url:'https://gestion360.jfconnect.online/admin/sistemas/jf-geoplan-360/'},
  {name:'JF CONNECT · Orquestador n8n',description:'Administración de flujos automatizados; credenciales privadas',url:'https://n8n.jfconnect.online/'},
  {name:'JF SOLUCIONES · GitHub público',description:'Repositorio de prototipos y documentación pública',url:'https://github.com/JFSOLUCIONES/JFSOLUCIONES'},
  {name:'JF GeoPlan · Portal de ingenieros',description:'No publicado ni validado: debe utilizar autenticación de cada cliente',url:''},
  {name:'JF GeoPlan · Portal de clientes',description:'Pendiente de backend y aislamiento de organizaciones',url:''},
];
const SUPPLIERS=[
  {name:'DURAGRASS Perú',category:'GRASS DEPORTIVO',region:'Perú · cobertura nacional declarada',url:'https://duragrassperu.com/',description:'Referencia publicada: PRO 50 instalado desde S/ 115/m². Confirmar el alcance para Ferreñafe.'},
  {name:'SISSA Perú',category:'MATERIAL / ROLLOS',region:'Lima · despacho sujeto a cotización',url:'https://www.sissaperu.com/grass-sintetico/',description:'Referencia de material deportivo S/ 32–55/m², no instalado.'},
  {name:'ICSEGRAS',category:'GRASS / INSTALACIÓN',region:'Cobertura nacional por confirmar',url:'https://www.icsegrass.com/',description:'Proveedor para una tercera propuesta técnica de césped; sin cotización verificada.'},
  {name:'CYPE · Generador de precios',category:'APU / INGENIERÍA',region:'Referencia de partidas Perú',url:'https://peru.generadordeprecios.info/',description:'Ayuda a preparar análisis de precios unitarios; verificar vigencia y condiciones.'},
  {name:'QGIS',category:'GIS CÓDIGO ABIERTO',region:'Software · escritorio',url:'https://qgis.org/',description:'Topografía, cartografía, CRS, capas y geoprocesamiento profesional.'},
  {name:'ezdxf',category:'CAD CÓDIGO ABIERTO',region:'Software · Python',url:'https://ezdxf.mozman.at/',description:'Motor para crear y analizar DXF desde archivos de coordenadas.'},
];
function navigate(tab){
  if(!$('screen-'+tab))return;
  active=tab;
  document.querySelectorAll('.screen').forEach(x=>x.classList.toggle('active',x.id==='screen-'+tab));
  document.querySelectorAll('.nav-btn').forEach(x=>x.classList.toggle('active',x.dataset.tab===tab));
  document.querySelector('.sidebar')?.classList.remove('open');
  window.scrollTo({top:0,behavior:'instant'});
}
function setupNavigation(){
  document.querySelectorAll('[data-tab],[data-open],[data-go]').forEach(el=>el.addEventListener('click',event=>{event.preventDefault();navigate(el.dataset.tab||el.dataset.open||el.dataset.go)}));
  $('toggleMenu')?.addEventListener('click',()=>document.querySelector('.sidebar')?.classList.toggle('open'));
}
function el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
function renderPlan(){
  const type=$('pitchVariant').value;
  const w=Number($('plotWidth').value),h=Number($('plotLength').value);
  try{
    const d=layoutTwoPitches(w,h,type);
    $('plotArea').textContent=fmt(d.plotArea)+' m²';$('playingArea').textContent=fmt(d.playingArea)+' m²';$('requiredWidth').textContent=fmt(d.requiredWidth)+' m';$('requiredLength').textContent=fmt(d.requiredLength)+' m';
    $('fitMessage').textContent=d.fits?'✓ Las dos canchas encajan geométricamente en el lote rectangular simulado. NO es conformidad municipal ni técnica.':`✕ Dimensiones insuficientes. Mínimo geométrico: ${fmt(d.requiredWidth)} × ${fmt(d.requiredLength)} m (sin estacionamientos y otras necesidades por verificar).`;
    $('fitMessage').classList.toggle('fail',!d.fits);
    const svg=$('planSvg');svg.replaceChildren();
    const NS='http://www.w3.org/2000/svg';const add=(tag,atts,text)=>{const n=document.createElementNS(NS,tag);for(const [k,v]of Object.entries(atts||{}))n.setAttribute(k,String(v));if(text)n.textContent=text;svg.append(n);return n;};
    const p=24,scale=Math.min(520/w,380/h);if(scale<=0)return;
    const sx=x=>p+x*scale,sy=y=>p+y*scale;
    add('rect',{x:sx(0),y:sy(0),width:w*scale,height:h*scale,fill:'#eff5e8',stroke:'#23526c','stroke-width':2,rx:6});
    add('rect',{x:sx(0),y:sy(0),width:w*scale,height:12*scale,fill:'#e1e8f0',opacity:.9});
    add('text',{x:sx(w/2),y:sy(6),fill:'#44647b','font-size':Math.min(13,9*scale/3),'text-anchor':'middle','font-weight':700},'ÁREA DE SERVICIOS / ACCESO');
    if(d.fits){d.pitches.forEach((pitch,i)=>{
      add('rect',{x:sx(pitch.x-2),y:sy(pitch.y-2),width:(pitch.width+4)*scale,height:(pitch.length+4)*scale,fill:'#d3e6c5',stroke:'#96ad7e','stroke-dasharray':'4 4'});
      add('rect',{x:sx(pitch.x),y:sy(pitch.y),width:pitch.width*scale,height:pitch.length*scale,fill:i?'#109b85':'#168c74',stroke:'#e9fffd','stroke-width':1.5,rx:1});
      add('line',{x1:sx(pitch.x+pitch.width/2),y1:sy(pitch.y),x2:sx(pitch.x+pitch.width/2),y2:sy(pitch.y+pitch.length),stroke:'#d1e9dc','stroke-width':1});
      add('circle',{cx:sx(pitch.x+pitch.width/2),cy:sy(pitch.y+pitch.length/2),r:Math.min(14,pitch.width*scale/8),fill:'none',stroke:'#d1e9dc','stroke-width':1.5});
      add('text',{x:sx(pitch.x+pitch.width/2),y:sy(pitch.y+pitch.length/2)+5,fill:'#fff','font-size':Math.min(13,Math.max(9,scale*1.8)),'text-anchor':'middle','font-weight':800},`CANCHA ${i+1}`);
    });}
    else add('text',{x:sx(w/2),y:sy(h/2),fill:'#a54935','font-size':15,'text-anchor':'middle','font-weight':800},'NO CABEN 2 CANCHAS');
    add('text',{x:25,y:448,fill:'#64869c','font-size':11},`Hipótesis ${d.label} · perímetro desconocido · orientación no verificada`);
  }catch(err){$('fitMessage').textContent=err.message;$('fitMessage').classList.add('fail');$('planSvg').replaceChildren();}
}
function renderFinance(){
 try{const variant=DEMO_VARIANTS[$('financeVariant').value];const x=finance({hourlyRate:Number($('hourlyRate').value),hoursPerPitch:Number($('dailyHours').value),monthlyRent:Number($('monthlyRent').value),investment:variant.investment});
 $('investmentOutput').textContent=money(variant.investment);$('salesOutput').textContent=money(x.revenue);$('cashOutput').textContent=money(x.cashflow);$('cashOutput').style.color=x.cashflow<0?'#ad443d':'#184c78';$('paybackOutput').textContent=x.payback?fmt(x.payback)+' años':'No recuperable';
 }catch(err){$('paybackOutput').textContent='Datos inválidos';}
}
function exportBlob(text,name,type){const url=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1500);}
function poly(){try{const p=parsePlanarPoints($('coordinateInput').value);const m=calculatePlanarPolygon(p);$('polyResult').textContent=`Polígono de ejemplo: ${fmt(m.area)} m² y ${fmt(m.perimeter)} m de perímetro (${m.points} vértices). Sólo válido si las coordenadas están en un sistema plano métrico correcto.`;return p;}catch(err){$('polyResult').textContent='Error: '+err.message;return null;}}
function setupTopography(){
 $('pitchVariant').addEventListener('change',()=>{const v=DEMO_VARIANTS[$('pitchVariant').value];$('plotWidth').value=v.minPlotWidth;$('plotLength').value=v.minPlotLength;renderPlan()});
 $('calculatePitch').addEventListener('click',renderPlan);$('calculatePoly').addEventListener('click',poly);
 $('downloadDXF').addEventListener('click',()=>{const p=poly();if(p)exportBlob(exportDXFR12(p),'JF_GEOPLAN_POLIGONO_DEMO.dxf','application/dxf')});renderPlan();
 $('financeCalc').addEventListener('click',renderFinance);$('financeVariant').addEventListener('change',renderFinance);renderFinance();
}
function supplierCards(){const root=$('supplierGrid');SUPPLIERS.forEach(x=>{const card=el('article','supplier-card');card.append(el('div','category',x.category),el('h3','',x.name),el('small','',x.region),el('p','',x.description));if(safeCatalogUrl(x.url)){const a=el('a','','Consultar fuente externa →');a.href=x.url;a.target='_blank';a.rel='noopener noreferrer';card.append(a)}root.append(card)});
 $('copyRFQ').addEventListener('click',async()=>{const msg=`SOLICITUD DE COTIZACIÓN – JF SOLUCIONES / FERREÑAFE\nProyecto: dos canchas de grass sintético para alquiler. Requerimos propuesta separada fútbol 6 (2 x 40×25 m) y fútbol 7 (2 x 50×30 m). Cotizar por m²; ficha técnica, dtex, altura de hilo, peso, drenaje, relleno, seguridad, transportes a Ferreñafe, instalación, base, garantías, mantenimiento, impuestos y plazos. No hay planos definitivos ni metrado validado. Favor detallar vigencia de la oferta y condiciones de pago.`;try{await navigator.clipboard.writeText(msg);$('rfqNotice').textContent='Plantilla de cotización copiada. Envío a cargo de un responsable autorizado.';}catch{$('rfqNotice').textContent=msg;}});
}
function makeChecks(id,arr){const root=$(id);for(const item of arr){const label=el('label','check-row');const input=document.createElement('input');input.type='checkbox';label.append(input,el('span','',item));root.append(label);}}
function renderLinks(){const root=$('linksTable');for(const entry of OPEN_LINKS){const row=el('div','link-row'),left=el('div');left.append(el('b','',entry.name),el('small','',entry.description));row.append(left);const valid=safeCatalogUrl(entry.url);if(valid){const a=el('a','','Abrir enlace verificado →');a.href=valid;a.target='_blank';a.rel='noopener noreferrer';row.append(a);}else row.append(el('span','tag tag-warning','Sin URL aprobada'));root.append(row)}}
setupNavigation();setupTopography();supplierCards();renderLinks();
makeChecks('fieldChecks',['Partida registral y levantamiento de linderos','Nivelación del terreno y pendientes reales','Estudio de mecánica de suelos según RNE aplicable','Investigación de drenaje pluvial y agua freática','Compatibilidad municipal para deporte y restaurante','Seguridad vial y acceso desde la carretera','Estudio fotométrico y seguridad eléctrica','Proyecto sanitario y accesibilidad','Firmas y responsabilidad de profesionales habilitados']);
makeChecks('successionChecks',['Constituir y documentar titularidad empresarial de dominios y repositorios','Designar administrador principal y suplente con base legal','Configurar cuentas individuales y autenticación multifactor','Guardar claves de recuperación cifradas en custodia offline','Inventariar cada sistema, URL MASTER y portal cliente','Mantener repositorios privados por proyecto y backups separados','Probar restauración aislada de PostgreSQL, n8n y archivos','Registrar proveedores, renovaciones, dominios y contratos','Auditar accesos cuando se active un proceso de sucesión']);
