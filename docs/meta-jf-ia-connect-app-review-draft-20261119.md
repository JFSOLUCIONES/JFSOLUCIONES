# JF IA Connect — Borrador de revisión de permisos Meta
Fecha: 2026-11-19
App ID: 3048029102034110
Estado observado en pantalla aportada por administrador: revisión NO ENVIADA.
Uso: JF CONNECT AI, plataforma de atención y gestión de WhatsApp Business para múltiples empresas.
ESTE DOCUMENTO NO CONSTITUYE APROBACIÓN NI PRESENTACIÓN DE SOLICITUD.

## whatsapp_business_messaging
JF CONNECT AI facilita a negocios que conceden expresamente acceso la recepción, clasificación y respuesta a sus conversaciones de WhatsApp Business mediante Meta Cloud API, por cuenta del negocio. Se utiliza para prestar soporte, atender consultas comerciales, registrar solicitudes y derivar a un asesor cuando corresponde. Los mensajes se procesan solo para el negocio propietario de la cuenta autorizada y bajo sus controles de privacidad, opt-in y ventanas de mensajería.

Demostración propuesta:
1. Empresa administradora autoriza explícitamente su WABA.
2. Un número de prueba envía un mensaje de servicio al número empresarial autorizado.
3. Se ve la entrada en n8n, el enrutamiento aislado a tenant y el registro CRM.
4. Mostrar respuesta de prueba al mismo usuario sin datos de terceros.
5. Mostrar control de duplicados, límites de mensajería y baja de comunicaciones.

## whatsapp_business_management
Necesario para recuperar, identificar y administrar los activos de WhatsApp Business autorizados por cada administrador: WABA, phone_number_id, estado de números, configuraciones y recursos que estén permitidos por los alcances concedidos. La plataforma utiliza estos identificadores para enrutar mensajes al agente del cliente correcto, evitar contaminación de datos y verificar el estado de la conexión.

Demostración propuesta:
1. Iniciar alta empresarial con consentimiento.
2. Mostrar que se consulta exclusivamente la WABA que el cliente ha autorizado.
3. Registrar WABA ID, phone number ID y estado en el panel privado.
4. Mostrar desconexión/revocación y aislamiento respecto de otras empresas.

## business_management
Solicitar únicamente si la función real de Embedded Signup / administración de activos empresariales lo requiere conforme a la revisión vigente de Meta. Serviría para identificar activos empresariales autorizados durante la incorporación, vincularlos al tenant correcto y administrar permisos que el propio negocio haya concedido. No se utilizará para acceder a activos de empresas que no hayan autorizado el acceso.

Demostración propuesta:
1. Administrador inicia sesión y aprueba el enlace de incorporación.
2. La aplicación obtiene exclusivamente activos autorizados.
3. Comprobar separación entre dos negocios distintos.
4. Mostrar mecanismo de revocación.

## public_profile
Uso mínimo de datos públicos del perfil que inicia sesión para identificar visualmente al administrador durante el procedimiento de autorización, de acuerdo con los campos efectivamente concedidos. No se asume acceso a datos privados ni se usa como fuente de prospección.

## Prerrequisitos y controles
- Comprobar requisitos, alcance y necesidad exacta de cada permiso en la interfaz de revisión, sin pedir permisos innecesarios.
- No solicitar aprobación con una demo ficticia presentada como real. Debe haber grabación verificable del flujo funcionando.
- Verificar correo de soporte, política de privacidad, eliminación de datos, condiciones de servicio y URL pública válidas.
- Documentar almacenamiento seguro, aislamiento por cliente, cifrado, mínimo acceso, logs sin tokens, firma X-Hub-Signature-256 y eliminación/revocación.
- Corregir OAuth actual, que tiene WABA AM-MEDIC hardcoded, antes de demostrar un alta multicliente.
- Verificar Embedded Signup y los requisitos de Meta para operar como proveedor tecnológico de terceros.
- No generar tokens ni pegar App Secret en documentación o chat.
- Hacer una prueba real end-to-end solo con cuenta, número y consentimiento autorizados.
- Enviar revisión únicamente después de verificar todos los requisitos y con aprobación del administrador.

## Estado técnico actual
- Windsor.ai confirma cuenta publicitaria Consultoría JF, pero eso NO autoriza administrar Meta for Developers.
- Flujo n8n OAuth JF IA Connect: NY8XzAcx6pVzsBBX (activo; referencias específicas a AM-MEDIC).
- Flujo WhatsApp Central: iEvozsVNjK5g2Dgg (activo; no modificar sin HMAC y rollback).
- QA onboarding multicliente: TnSdU8F97b4SztY2 (inactivo; solo datos ficticios).
- Tabla de control: JF_META_CLIENT_ONBOARDING_V1.
