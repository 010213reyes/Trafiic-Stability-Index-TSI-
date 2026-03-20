# Estructura del proyecto (TSI)

Este documento resume cómo está organizado actualmente el proyecto desde la raíz.

## Árbol de carpetas

```text
TSI/
├─ README.md
├─ README_STRUCTURE.md
├─ data/
│  ├─ raw/
│  │  ├─ scraped_traffic.csv
│  │  └─ traffic_data.csv
│  └─ processed/
│     └─ traffic_data.csv
├─ notebooks/
│  ├─ Scraping_Traffic.ipynb
│  └─ Data_Ingestion_Basic_Procesing.ipynb
├─ .venv/
├─ .gitignore
├─ .git/
└─ tsi/ (vacía, pendiente de eliminar)
```

## Qué va en cada carpeta

- `data/raw/`: datos originales o recién recolectados (sin procesamiento final).
- `data/processed/`: datos limpios/transformados listos para análisis.
- `notebooks/`: notebooks principales del pipeline y análisis.
- `.venv/`: entorno virtual local de Python.

## Flujo recomendado

1. Ejecutar `notebooks/Scraping_Traffic.ipynb` para generar/actualizar datos en `data/raw/`.
2. Ejecutar `notebooks/Data_Ingestion_Basic_Procesing.ipynb` para limpiar/procesar y guardar en `data/processed/`.

## Limpieza pendiente

La carpeta `tsi/` está vacía y se puede eliminar cuando no esté bloqueada por VS Code o OneDrive.

Comando (PowerShell):

```powershell
Remove-Item -Path "./tsi" -Recurse -Force
```
