import requests

OCR_URL = 'https://api.ocr.space/parse/image'

def leer_imagen(api_key, ruta_imagen):
    if not api_key:
        raise ValueError('Falta la API key de OCR.space.')
    with open(ruta_imagen, 'rb') as f:
        r = requests.post(OCR_URL, files={'filename': f}, data={
            'apikey': api_key,
            'language': 'spa',
            'OCREngine': 2,
            'scale': True,
            'isOverlayRequired': False,
        }, timeout=90)
    r.raise_for_status()
    data = r.json()
    if data.get('IsErroredOnProcessing'):
        msg = data.get('ErrorMessage') or data.get('ErrorDetails') or 'Error OCR'
        raise RuntimeError(str(msg))
    resultados = data.get('ParsedResults') or []
    if not resultados:
        return ''
    return '\n'.join((x.get('ParsedText') or '') for x in resultados)
