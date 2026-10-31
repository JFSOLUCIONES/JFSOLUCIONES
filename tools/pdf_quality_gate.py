#!/usr/bin/env python3
"""NO+ preflight editorial: detecta borradores no aptos para distribución."""
import argparse, json, sys
from pathlib import Path
try:
    import fitz
except ImportError as exc:
    raise SystemExit("Instalar primero PyMuPDF: python -m pip install pymupdf") from exc

def inspect_pdf(path: str, min_words: int = 5500, min_photo_pages: int = 7) -> dict:
    doc = fitz.open(path)
    words = []
    pages = []
    photos = set()
    for idx, p in enumerate(doc):
        text = p.get_text("text")
        count = len(text.split())
        words.append(count)
        image_items=[]
        for info in p.get_images(full=True):
            xref = info[0]
            pix=doc.extract_image(xref)
            width,height = pix["width"],pix["height"]
            # Logos y pictogramas pequeños no cuentan como fotografía editorial.
            if width >= 700 and height >= 450:
                photos.add(idx+1)
                image_items.append({"w":width,"h":height,"xref":xref})
        pages.append({"page":idx+1,"words":count,"photo_candidates":image_items})
    total=sum(words)
    issues=[]
    if len(doc)!=12: issues.append("La edición necesita exactamente 12 páginas")
    if total<min_words: issues.append(f"Texto demasiado breve: {total} palabras (mínimo editorial objetivo {min_words})")
    if len(photos)<min_photo_pages: issues.append(f"Fotografía editorial insuficiente: {len(photos)} páginas con imágenes de tamaño relevante (objetivo {min_photo_pages})")
    sparse=[p["page"] for p in pages[1:] if p["words"]<250 and not p["photo_candidates"]]
    if sparse: issues.append(f"Páginas interiores sin suficiente contenido ni foto: {sparse}")
    result={
        "file": str(path),"pages":len(doc),"words_total":total,
        "photo_pages":len(photos),"photo_page_numbers":sorted(photos),
        "page_details":pages,"automated_gate":"PASS" if not issues else "FAIL",
        "issues":issues,
        "notes":[
            "Este control NO determina veracidad, licencia, procedencia ni autenticidad de fotos.",
            "Una fotografía generada con IA puede pasar el umbral técnico; debe bloquearse en revisión humana.",
            "Solo un editor puede autorizar distribución tras corroborar fuentes, derechos y diseño de impresión."
        ]}
    doc.close()
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--min-words",type=int,default=5500)
    parser.add_argument("--min-photo-pages",type=int,default=7)
    parser.add_argument("--report",default="")
    args=parser.parse_args()
    result=inspect_pdf(args.pdf,args.min_words,args.min_photo_pages)
    payload=json.dumps(result,ensure_ascii=False,indent=2)
    print(payload)
    if args.report: Path(args.report).write_text(payload,encoding="utf-8")
    if result["automated_gate"]!="PASS": sys.exit(2)
