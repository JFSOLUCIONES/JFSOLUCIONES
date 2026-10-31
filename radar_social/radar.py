#!/usr/bin/env python3
"""NO+ Radar Social: lector RSS/Atom autorizado, sin publicación ni sesiones privadas."""
import argparse
import hashlib
import ipaddress
import json
import re
import socket
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html import unescape
from urllib.parse import urlsplit

USER_AGENT = "NOMasRadar/0.1 (+https://periodiconomas.space)"
MAX_BYTES = 750_000
ALLOWED = {"facebook", "instagram", "tiktok", "youtube", "telegram", "mastodon", "web", "otros"}
TOPICS = {
    "fiscalizacion": r"corrupci[oó]n|contralor[ií]a|licitaci[oó]n|seace|presunt[oa]|denuncia|sobrevaloraci[oó]n|colusi[oó]n",
    "politica": r"alcalde|gobernador|congreso|consejo regional|elecci[oó]n|concejo|ministerio",
    "salud": r"hospital|dengue|vacunaci[oó]n|salud|epidemia",
    "economia": r"empleo|inflaci[oó]n|inversi[oó]n|agro|comercio|mercado",
    "deportes": r"f[uú]tbol|partido|selecci[oó]n|campeonato|atleta",
    "tecnologia": r"tecnolog[ií]a|ciberseguridad|inteligencia artificial|internet|software",
}

def public_https_url(url: str) -> bool:
    try:
        p = urlsplit(url)
        if p.scheme != "https" or not p.hostname or p.username or p.password:
            return False
        if p.port not in (None, 443):
            return False
        host = p.hostname.lower()
        if host == "localhost" or host.endswith((".local", ".internal")):
            return False
        try:
            ip = ipaddress.ip_address(host.strip("[]"))
            return ip.is_global
        except ValueError:
            return True
    except ValueError:
        return False

def validate_dns(host: str) -> None:
    """Evita destinos localhost, LAN, link-local y metadatos de nube."""
    for info in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM):
        address = info[4][0]
        if not ipaddress.ip_address(address).is_global:
            raise ValueError("Destino no público rechazado")

def sanitize(value: str, max_length: int = 700) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(value)).strip()[:max_length]

def text(parent, *tags):
    for tag in tags:
        n = parent.find(tag)
        if n is not None and (n.text or "").strip():
            return n.text or ""
    return ""

def parse_feed(xml_data: bytes, source: dict) -> list[dict]:
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")
    if not items:
        ns = "{http://www.w3.org/2005/Atom}"
        items = root.findall(f".//{ns}entry")
    out = []
    for item in items[:100]:
        title = sanitize(text(item, "title", "{http://www.w3.org/2005/Atom}title"))
        url = text(item, "link")
        if not url:
            link = item.find("{http://www.w3.org/2005/Atom}link")
            url = link.get("href", "") if link is not None else ""
        if not public_https_url(url):
            continue
        summary = sanitize(text(item, "description", "summary", "{http://www.w3.org/2005/Atom}summary"), 1400)
        date = sanitize(text(item, "pubDate", "{http://www.w3.org/2005/Atom}updated", "{http://www.w3.org/2005/Atom}published"), 90)
        combined = (title + " " + summary).lower()
        tags = [topic for topic, expression in TOPICS.items() if re.search(expression, combined, re.I)]
        dedupe_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
        out.append({
            "id": dedupe_id,
            "title": title,
            "url": url,
            "summary": summary,
            "published_at_source": date,
            "source": source["name"],
            "platform": source["platform"],
            "region": source.get("region", "sin_asignar"),
            "topics": tags or ["general"],
            "score_preliminar": min(10, 1 + len(tags) * 2 + (3 if "fiscalizacion" in tags else 0)),
            "status": "PENDIENTE_VERIFICACION",
            "approved": False,
            "autopublish": False,
        })
    return out

def download_feed(url: str) -> bytes:
    if not public_https_url(url):
        raise ValueError("Solo URLs HTTPS públicas")
    host = urlsplit(url).hostname
    validate_dns(host)
    # No seguir redirecciones para impedir cambios no verificados de destino.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, text/xml, application/xml"})
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(req, timeout=12) as response:
        if response.status != 200:
            raise ValueError("HTTP distinto de 200")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Fuente supera límite de tamaño")
        return data

def run(source_file: str, output_file: str) -> dict:
    sources = json.load(open(source_file, encoding="utf-8"))["sources"]
    seen, findings, failures = set(), [], []
    for s in sources:
        if not s.get("enabled") or not s.get("authorized"):
            continue
        if s.get("platform") not in ALLOWED:
            failures.append({"source": s.get("name", "?"), "error": "Plataforma inválida"})
            continue
        try:
            records = parse_feed(download_feed(s["url"]), s)
            for item in records:
                if item["id"] not in seen:
                    findings.append(item)
                    seen.add(item["id"])
        except (ValueError, OSError, ET.ParseError, urllib.error.URLError) as exc:
            failures.append({"source": s.get("name", "?"), "error": str(exc)[:160]})
    findings.sort(key=lambda x: (-x["score_preliminar"], x["title"]))
    result = {"generated_at": datetime.now(timezone.utc).isoformat(), "count": len(findings), "findings": findings, "errors": failures, "notice": "Hallazgos sin corroborar: prohibida publicación automática"}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--sources", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    result = run(args.sources, args.output)
    print(json.dumps({"hallazgos": result["count"], "errores": result["errors"]}, ensure_ascii=False))
