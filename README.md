# Compresor OCR PRO

Aplicación Windows para comprimir imágenes, reconocer números de Registro mediante OCR.space y renombrar copias sin modificar los originales.

## Ejecutar
```bash
pip install -r requirements.txt
python main.py
```

## OCR
Obtenga una API key de OCR.space y péguela en la aplicación. También puede definir `OCR_SPACE_API_KEY` como variable de entorno.

## Salida
Se crea `IMAGENES_PROCESADAS` dentro de la carpeta seleccionada.

## EXE
El workflow de GitHub Actions genera un ZIP con la aplicación Windows en la sección Artifacts de la ejecución.
