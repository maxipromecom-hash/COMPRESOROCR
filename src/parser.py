import re

REG_PATTERNS = [
    re.compile(r'(?i)\bR\s*[-–—]?\s*(\d{2,7})\s*[/\\\-]\s*(\d{2})\b'),
    re.compile(r'(?i)\bREG(?:ISTRO)?\s*[:Nº°\.\- ]*R?\s*[-–—]?\s*(\d{2,7})\s*[/\\\-]\s*(\d{2})\b'),
]

def detectar_registro(texto: str):
    if not texto:
        return None
    t = texto.replace('—','-').replace('–','-').replace('|','/').replace('\\','/')
    # common OCR confusion near the R prefix
    t = re.sub(r'(?i)\b[Řℝ]\b', 'R', t)
    for p in REG_PATTERNS:
        m = p.search(t)
        if m:
            return f"R-{m.group(1)}/{m.group(2)}"
    return None

def nombre_seguro(nombre: str):
    return re.sub(r'[<>:"/\\|?*]', '-', nombre).strip().rstrip('.')
