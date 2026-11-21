/** JF Gestión360 | MASTER/cliente — contrato de acceso para backend seguro.
 *  PROTOTIPO: consultar roles y permisos SOLO desde sesión firmada del servidor.
 */
export function normaliseLink(raw) {
  if (typeof raw !== 'string' || raw.length>2048 || raw.trim()!==raw) return null;
  try {
    const url=new URL(raw);
    if (url.protocol!=='https:' || url.username || url.password || url.search || url.hash) return null;
    if (!url.hostname || url.hostname==='localhost' || url.hostname.endsWith('.local')) return null;
    return url.href;
  }catch{return null;}
}
export function linksForActor(actor, assets) {
  if(!actor || actor.authenticated!==true || typeof actor.id!=='string' || !actor.id || !Array.isArray(assets)) return [];
  const isEnterpriseMaster=actor.role==='master' && actor.enterpriseApproved===true;
  const isLegalSuccessor=actor.role==='successor' && actor.legalActivationApproved===true && actor.enterpriseApproved===true;
  const isClient=actor.role==='client' && typeof actor.tenantId==='string' && actor.tenantId.length>0;
  if(!isEnterpriseMaster&&!isLegalSuccessor&&!isClient) return [];
  const result=[];
  for(const a of assets){
    if(!a || typeof a!=='object' || a.archived===true)continue;
    const id=String(a.systemId||'');if(!id)continue;
    const permissions=isEnterpriseMaster||isLegalSuccessor;
    if(permissions && a.enterpriseEnabled===true){
      for(const kind of ['master','operative']){
        const url=normaliseLink(a[kind+'Url']);
        if(url && a[kind+'Approved']===true)result.push({systemId:id,kind,url});
      }
    }
    if(isClient && a.tenantId===actor.tenantId && a.clientEnabled===true && a.clientApproved===true){
      const url=normaliseLink(a.clientUrl);
      if(url)result.push({systemId:id,kind:'client',url});
    }
  }
  return result;
}
export function catalogSummary(assets){
  if(!Array.isArray(assets))throw new TypeError('Catálogo debe ser lista');
  let master=0,client=0,operational=0;
  for(const item of assets){
    if(normaliseLink(item?.masterUrl))master++;
    if(normaliseLink(item?.clientUrl))client++;
    if(normaliseLink(item?.operativeUrl))operational++;
  }
  return {assets:assets.length,syntacticallyValid:{master,client,operational},note:'La sintaxis válida no confirma disponibilidad ni autorización'};
}
