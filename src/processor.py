from pathlib import Path
from PIL import Image, ImageOps
from .ocr import leer_imagen
from .parser import detectar_registro, nombre_seguro

EXTS = {'.jpg','.jpeg','.png','.bmp','.tif','.tiff'}
QUALITY = {'Alta': 88, 'Media': 75, 'Máxima compresión': 58}

def listar_imagenes(carpeta):
    return [p for p in Path(carpeta).iterdir() if p.is_file() and p.suffix.lower() in EXTS]

def comprimir(origen: Path, destino: Path, nivel='Media', max_dim=2200):
    destino.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(origen) as im:
        im = ImageOps.exif_transpose(im)
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        ext = destino.suffix.lower()
        if ext in {'.jpg','.jpeg'}:
            if im.mode not in ('RGB','L'):
                im = im.convert('RGB')
            im.save(destino, 'JPEG', quality=QUALITY[nivel], optimize=True, progressive=True)
        elif ext == '.png':
            im.save(destino, 'PNG', optimize=True, compress_level=9)
        elif ext in {'.tif','.tiff'}:
            im.save(destino, 'TIFF', compression='tiff_lzw')
        else:
            im.save(destino)

def procesar_archivo(origen, salida, api_key, hacer_ocr, hacer_compresion, nivel):
    origen = Path(origen); salida = Path(salida)
    registro = None
    texto = ''
    if hacer_ocr:
        texto = leer_imagen(api_key, str(origen))
        registro = detectar_registro(texto)
    stem = nombre_seguro(registro) if registro else origen.stem
    destino = salida / f'{stem}{origen.suffix.lower()}'
    n = 2
    while destino.exists():
        destino = salida / f'{stem} ({n}){origen.suffix.lower()}'
        n += 1
    if hacer_compresion:
        comprimir(origen, destino, nivel)
    else:
        import shutil
        salida.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origen, destino)
    return registro, destino, texto
