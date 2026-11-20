import {createHmac, timingSafeEqual} from "node:crypto";

/**
 * JF CONNECT — perimeter verification for Meta WhatsApp POST.
 * Must run BEFORE parsing/routing messages, using exact raw HTTP bytes.
 * Secrets come from server-side secret manager, never webhook payload.
 */
export function verifyMetaPost({rawBody, signatureHeader, appSecret}) {
  if (!(Buffer.isBuffer(rawBody) || rawBody instanceof Uint8Array)) return false;
  if (typeof appSecret!=="string" || appSecret.length<16) return false;
  if (typeof signatureHeader!=="string" || !/^sha256=[a-fA-F0-9]{64}$/.test(signatureHeader)) return false;
  const expected=createHmac("sha256",appSecret).update(rawBody).digest();
  const actual=Buffer.from(signatureHeader.slice(7),"hex");
  return actual.length===expected.length && timingSafeEqual(actual,expected);
}

/** Source of truth must be an authenticated business account -> phone_number_id mapping. */
export function routeJfSales({signatureValid, phoneNumberId, allowlistedPhoneNumberIds, message, idempotentClaimed}) {
  if (signatureValid!==true) return {route:"DENY_UNVERIFIED"};
  if (typeof phoneNumberId!=="string" || !/^\d{6,25}$/.test(phoneNumberId)) return {route:"DENY_BAD_PHONE_ID"};
  if (!(allowlistedPhoneNumberIds instanceof Set) || !allowlistedPhoneNumberIds.has(phoneNumberId))
    return {route:"PRESERVE_EXISTING_BOT"};
  if (idempotentClaimed!==true) return {route:"IGNORE_DUPLICATE_OR_UNCLAIMED"};
  if (typeof message!=="string" || !message.trim()) return {route:"NO_MESSAGE"};
  return {route:"JF_SALES",mode:"QUOTE_DRAFT_ONLY",externalSendingEnabled:false};
}
