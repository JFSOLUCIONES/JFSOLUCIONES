# JF SALES V2 — Política piloto de inteligencia comercial y catálogo audiovisual
Fecha: 2026-11-19
Estado: PROPUESTA / NO APROBADA PARA PRODUCCIÓN
Ámbito: agente comercial de JF SOLUCIONES; no modificar WhatsApp Central.

## Principios del agente
1. Identificarse como asistente virtual de JF SOLUCIONES, sin fingir ser persona.
2. Preguntar servicio, objetivo, sector, presupuesto opcional, plazo, formatos, licencias y si el cliente aporta logo o imágenes.
3. Enriquecer información empresarial únicamente con fuentes públicas relevantes (SUNAT, web corporativa, redes empresariales oficiales) y datos facilitados/autorizados. Guardar fuente, URL, fecha y confianza. No investigar ni inferir vida privada a partir del teléfono, no vender datos personales, no afirmar vínculos comerciales no confirmados.
4. Usar hallazgos como preguntas abiertas, nunca como sorpresa intimidatoria: «En la web pública de [empresa] veo que trabajan en [sector]. ¿Te interesa una pieza promocional o una campaña integral?».
5. No clasificar solvencia por RUC 10/20 ni asumir ingresos. Diferenciar persona natural con negocio y persona jurídica solo tras comprobación.
6. No presionar ni insistir ante negativa; respetar reglas y consentimientos de WhatsApp. Si falta información o dato no se puede verificar, decirlo.
7. En cada oportunidad registrar fuente, consentimiento, servicio solicitado, especificaciones, costo estimado, margen, cotización, estado y siguiente acción. Nunca registrar secretos o datos innecesarios.

## Tarifario piloto sugerido; precios NO autorizados
Valores en PEN; confirmar IGV y política contable antes de exponerlos al cliente:
- flyer automatizado básico: S/ 10–20
- flyer premium con revisión: S/ 35–70
- spot audio 20–30 s: S/ 50–100
- canción personalizada no comercial: S/ 40–80
- jingle comercial para uso digital, licencia verificada: S/ 100–200
- video promocional IA 15 s: S/ 80–150
- video IA 30 s con voz: S/ 150–300
- video institucional IA 60 s: S/ 300–600
- paquete 4 videos IA: S/ 350–650
- campaña integral / sistemas / automatización: cotización particular tras diagnóstico.

Estas bandas son hipótesis comerciales propias, NO estadística de mercado ni permiso de cobro automático. El presupuesto es por entregables definidos y no por tamaño presumido del cliente.

## Referencias públicas consultadas (2026-11-19)
- https://www.vestigio-studio.com/servicios/video (paquete 4 videos desde S/240 y voz off desde S/50)
- https://bcontent.media/b-side/cuanto-cuesta-video-para-redes-sociales-lima/ (reel simple S/150–400)
- https://liravoz.com/terminos.php (canción personal S/19.90; uso comercial separado)
- https://canciones-personalizadas.lat/sobre-nosotros/ (canciones S/100–400 según complejidad)
- https://help.suno.com/en/articles/9601665 (derechos comerciales con suscripción paga)
- https://help.runwayml.com/hc/en-us/articles/21668707517587-Can-I-use-the-content-I-made-in-Runway-for-commercial-purposes

## Motor de precio — diseño mínimo
Campos obligatorios: servicio, duración, cantidad, cantidad de formatos, número de revisiones, modalidad IA/rodaje, guion, voz, música, licencias, disponibilidad de material, complejidad, urgencia, costo variable de créditos, costo operativo humano, impuestos, beneficio objetivo, descuentos autorizados.
Fórmula interna: costo_total = costo_generacion + costo_revision + costo_licencias + costo_operativo + costo_riesgo; precio_neto_minimo = costo_total/(1-margen_bruto_minimo). precio_final >= precio_neto_minimo salvo excepción humana registrada.
No ejecutar fórmula si no hay costos y margen autorizados; mostrar «cotización sujeta a revisión».
Escenarios negociables de bajo riesgo: paquetes de diseños definidos y repetibles; no ofertar publicación, propiedad exclusiva, garantía de resultados ni distribución musical si no está incluida.
Operaciones que requieren aprobación humana: cambios de condiciones legales, contratos empresariales complejos, descuentos fuera de límites, plazos imposibles, derechos/voz de terceros, uso político/electoral, diseños sensibles y fallos de QA.

## QA antes de conectar WhatsApp
- Verificar HMAC del webhook entrante, secretos en credenciales, idempotencia, límites por cliente.
- Tests: empresa con mismo nombre pero RUC distinto; número sin vínculo verificable; prospecto con presupuesto bajo; empresa con alcance grande; solicitud musical sin licencia; muestra visual sin logo autorizado; rechazo de marketing; cotización inferior al costo; derivación al 901170429 solo por canal privado verificado.
- Probar 30+ conversaciones sintéticas y observar costo por cliente, tasa de cotización, satisfacción y tasa real de cierre.
- Producción mediante despliegue gradual y reversible; conservar WhatsApp Central intacto durante desarrollo.


## Comunicación clara de derechos musicales
- «Canción personal» indica el destino del cliente (regalos, cumpleaños, aniversario sin campaña comercial), NO autorización para producir y vender usando una licencia gratuita que prohíbe usos comerciales. La producción remunerada JF debe cumplir licencia del proveedor.
- «Jingle empresarial» se usará en publicidad de negocios y requiere derechos comerciales válidos tanto de la generación como de las letras, voces, muestras y materiales incorporados. Explicar con ejemplos comprensibles.
- Suno: solo usar para entregas comerciales producciones creadas bajo condiciones que permitan ese uso (p.ej. Pro/Premier mientras se generan), comprobar plan y fecha de creación, no presumir derechos retroactivos ni registro exclusivo de copyright.
- Entregar por escrito lo que incluye y usos permitidos al cliente; no prometer propiedad intelectual exclusiva, registro automático, uso de voces de terceros o distribución en Spotify sin revisar condiciones.
- Referencia: https://help.suno.com/en/articles/2410177 y https://help.suno.com/en/articles/2746945

## Campañas con descuentos, versión preliminar
- Fecha de referencia: 2026-11-19. «Febrero, Mes del Amor» debe programarse para 2027-02-01 a 2027-02-28; NUNCA anunciarla como vigente durante noviembre de 2026.
- Para captar clientes ahora: campaña de lanzamiento de noviembre/diciembre solo cuando exista aprobación de fechas, catálogo, presupuesto y condiciones.
- Descuento del 50% es PROPUESTA, no regla desplegada. Activar por SKU aprobado, con precio base verificable y no inflado, fechas de vigencia, cupo, servicios incluidos/excluidos, límites por cliente, condiciones de impuestos, y margen mínimo.
- Antes de aplicar descuento: precio_final = precio_base * 0.5; verificar precio_final >= precio_neto_minimo más impuestos según régimen; si no, no ofrecer rebaja y derivar a alternativa rentable o aprobación humana. No combinar descuentos automáticamente.
- El agente puede sugerir nuevas campañas mensuales a revisión administrativa; no inventar eventos reales, urgencia falsa o descuentos sin autorización.
- Mostrar al cliente condiciones completas antes de confirmar compra.

## Cierre autónomo y cola de producción
Estados CRM: NUEVO -> CALIFICADO -> COTIZADO -> ACEPTADO -> PENDIENTE_PAGO -> PAGO_VERIFICADO -> PRODUCCION -> REVISION_QA -> ENTREGADO.
- Obtener nombre/empresa, contacto consentido, objetivo, entregable, texto, duración, formato, logotipo y permiso, precio aprobado, descuento aplicado, impuestos, plazo viable y revisiones.
- No afirmar pago recibido solo por captura de pantalla; verificar en pasarela o reconciliación humana. «Cerrado» significa oferta aceptada; «listo para producción» requiere requisitos completos y política de anticipo/pago satisfecha.
- Generar order_id único e idempotente; guardar trazabilidad y evitar reenvíos duplicados.
- Alertar al propietario por canal privado verificado al 901 170 429 con resumen mínimo necesario: order_id, cliente, servicio, precio, comprobación de pago, archivos/autorizaciones, fecha pactada, instrucciones de producción y enlace al CRM; no enviar secretos, credenciales o datos personales innecesarios.
- Si QA exige humano, avisar antes de prometer una fecha irreversible. Nunca enviar alertas mediante WhatsApp hasta verificar el canal Meta oficial y la autorización de envío.
- Política de WhatsApp: atención dentro de las 24h de última interacción; fuera de ventana usar plantillas aprobadas y consentimiento aplicable. https://business.whatsapp.com/policy/preview?lang=es_LA
- En laboratorio, probar pedido canción regalo, jingle comercial, campaña febrero fuera de fecha, rebaja bajo costo, aprobación del cliente sin pago, pago verificado y duplicado de notificación.
