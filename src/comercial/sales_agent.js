// JF SOLUCIONES | Agente comercial V2 - motor seguro independiente, sin red ni envíos.
// Solo prepara decisiones para revisión. Nunca envía WhatsApp, investiga números ni cobra.
const canon = value => String(value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const sanitize = (value, max=320) => String(value ?? '').replace(/[\r\n\t]+/g,' ').trim().slice(0,max);
const has = (text, patterns) => patterns.some(p => p.test(text));

export function tipoRuc(ruc) {
  const v = String(ruc ?? '').replace(/\s/g,'');
  if (!/^\d{11}$/.test(v)) return 'NO_VERIFICADO';
  if(v.startsWith('10')) return 'PERSONA_NATURAL_POR_PREFIJO_NO_VERIFICADA';
  if(v.startsWith('20')) return 'PERSONA_JURIDICA_POR_PREFIJO_NO_VERIFICADA';
  return 'TIPO_NO_DETERMINADO';
}

export function calificarOportunidad(s={}) {
  // Solo señales suministradas por el interesado. NO perfila por RUC, teléfono,
  // presunta riqueza, localización exacta, datos sensibles ni redes personales.
  const a = {
    necesidad: s.necesidadClara === true ? 30 : 0,
    horizonte: ['esta_semana','este_mes'].includes(s.horizonte) ? 20 : 0,
    autoridad: s.participaDecision === true ? 15 : 0,
    alcance: s.alcanceDefinido === true ? 20 : 0,
    presupuesto: s.presupuestoDeclarado === true ? 15 : 0,
  };
  const puntaje = Object.values(a).reduce((acc,v)=>acc+v,0);
  return {puntaje,nivel:puntaje>=65?'ALTA':puntaje>=30?'MEDIA':'EXPLORATORIA',criterios:a};
}

export function calcularCotizacionBorrador({tarifario,servicio,unidades=1,complejidad=1,extras=0}={}) {
  const entry = tarifario?.[servicio];
  if(!entry || entry.aprobado !== true || !Number.isFinite(entry.precioBase) || entry.precioBase<=0)
    return {estado:'PENDIENTE_TARIFARIO_APROBADO',monto:null,requiereAprobacion:true};
  if(!Number.isInteger(unidades)||unidades<1||unidades>60||!Number.isFinite(complejidad)||complejidad<1||complejidad>3||
     !Number.isFinite(extras)||extras<0||extras>100000)
    return {estado:'ALCANCE_INVALIDO',monto:null,requiereAprobacion:true};
  const subtotal = Math.round((entry.precioBase * unidades * complejidad + extras)*100)/100;
  return {estado:'BORRADOR_NO_VINCULANTE',monto:subtotal,moneda:entry.moneda||'PEN',requiereAprobacion:true,fuente:'TARIFARIO_INTERNO_APROBADO'};
}

export function evaluarMensaje(e={}, policy={}) {
  const mensaje = sanitize(e.mensaje,2400), texto=canon(mensaje);
  const origen = sanitize(e.origen?.utm_source||e.origen?.campania||'',48);
  const tipo = tipoRuc(e.rucDeclarado);
  const noMolestar = has(texto,[/\b(no me escriban|no me contacten|no quiero mensajes|salir|cancelar suscripcion|baja)\b/]);
  const queja = has(texto,[/\b(reclamo|queja|denuncia|incumplimiento|hablar con alguien|hablar con asesor)\b/]);
  const seguridad = has(texto,[/\b(ignora instrucciones|transfiere dinero|pago inmediato|sin autorizacion|datos privados)\b/]);
  const diseno = has(texto,[/\b(flyer|diseno|logo|marca|publicidad|redes sociales|facebook|instagram|campana)\b/]);
  const automatizacion = has(texto,[/\b(n8n|whatsapp|chatbot|bot|automatiza|automatizacion|crm|integracion|ia)\b/]);
  const web = has(texto,[/\b(pagina web|sitio web|desarrollo web|landing)\b/]);
  const precio = has(texto,[/\b(precio|presupuesto|cotiz|cuanto cuesta|contratar|plan)\b/]);
  const curso = has(texto,[/\b(curso|hotmart|academia|capacitacion)\b/]);
  const oferta = noMolestar?'NO_CONTACTAR':seguridad?'REVISAR_SEGURIDAD':queja?'ATENCION_HUMANA':curso?'JF_ACADEMY':diseno?'MARKETING_DISENO':automatizacion?'AUTOMATIZACION_IA':web?'DESARROLLO_WEB':'DIAGNOSTICO';
  let respuesta='';
  const intro='Hola, soy el asistente virtual de JF SOLUCIONES. ';
  if(noMolestar) respuesta='Entendido. No enviaremos comunicaciones comerciales adicionales. Si necesitas algo en otro momento, puedes volver a escribirnos.';
  else if(seguridad) respuesta='Para tu seguridad, los pagos y contratos se confirman por canales oficiales con nuestro equipo. Voy a derivar esta solicitud a un asesor.';
  else if(queja) respuesta='Gracias por contarnos lo sucedido. Voy a solicitar atención de una persona del equipo. ¿Puedes describir brevemente el inconveniente?';
  else if(curso) respuesta='Tenemos guías gratuitas en https://jfconnect.online/academia.html. Los cursos pagados aún no están publicados. ¿Qué tema te gustaría aprender?';
  else if(diseno) respuesta='Podemos ayudarte con una pieza publicitaria adaptada a tu negocio. ¿Qué producto promocionas y cuál es la fecha de tu campaña? Si deseas, comparte tu logo y autoriza su uso únicamente para preparar una muestra.';
  else if(automatizacion) respuesta='Podemos automatizar consultas, captación y seguimiento comercial con WhatsApp oficial, IA y n8n. Para proponerte lo adecuado, ¿qué negocio tienes y qué tareas te quitan más tiempo?';
  else if(web) respuesta='Podemos crear una web para captar clientes y organizar tus servicios. ¿Ya tienes una página o comenzaríamos desde cero?';
  else if(precio) respuesta='Con gusto te preparamos un presupuesto según el trabajo real. ¿Qué servicio necesitas, qué alcance imaginas y cuándo te gustaría comenzar?';
  else respuesta='¿Tienes un negocio funcionando, estás empezando un emprendimiento o buscas asesoría para una idea? Cuéntame qué te gustaría lograr y buscamos una solución que se ajuste a tu etapa.';
  const score = calificarOportunidad(e.senales||{});
  const ahoraMs=Date.parse(policy.ahora||'');
  const inboundMs=Date.parse(policy.ultimoMensajeCliente||'');
  const ventanaAbierta=Number.isFinite(ahoraMs)&&Number.isFinite(inboundMs)&&ahoraMs>=inboundMs&&(ahoraMs-inboundMs)<86400000;
  const puedeResponder=policy.numeroMetaVerificado===true && policy.optInYBaseLegalVerificados===true && ventanaAbierta && !noMolestar && !seguridad;
  const rucConsulta = Boolean(e.rucDeclarado && e.autorizaConsultaRuc === true && tipo !== 'NO_VERIFICADO');
  const disenioSolicitud = Boolean(e.logoRecibido===true && e.autorizaUsoLogo===true && diseno);
  const derivacion=queja||seguridad||precio||score.nivel==='ALTA';
  return {
    version:'JF_SALES_V2_LAB',estado:'BORRADOR_SIN_ENVIO',intencion:oferta,leadScore:score,
    tipoRucDeclarado:tipo,rucRevisableConSUNAT:rucConsulta,origenDeclarado:origen||'NO_IDENTIFICADO',
    respuestaBorrador:intro+respuesta,requiereHumano:derivacion,crearBriefVisual:disenioSolicitud,
    crearCotizacionBorrador:precio,puedeResponderDentroVentana:puedeResponder,
    debeSolicitarConfirmacionAntesDeCobrar:true,avisarResponsable:derivacion,
    telefonoResponsable:'CONFIGURACION_PRIVADA',sinEnriquecimientoPorTelefono:true
  };
}
