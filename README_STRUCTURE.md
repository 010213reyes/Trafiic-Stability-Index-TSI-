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
│  ├─ Data_Ingestion_Basic_Procesing.ipynb
│  ├─ Realistic_Traffic_Modeling.ipynb
│  ├─ 01_Synthetic_Traffic_Data.ipynb
│  ├─ 02_Historical_Data_Import.ipynb
│  └─ 03_Crowdsourcing_Collection.ipynb
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

## Flujo recomendado (Pipeline de Recopilación)

**Técnicas de recopilación de datos (elegir una o varias):**

1. **Scraping_Traffic.ipynb** → Web scraping de fuentes públicas → `data/raw/`
2. **01_Synthetic_Traffic_Data.ipynb** → Generación de datos sintéticos realistas → `data/raw/`
3. **02_Historical_Data_Import.ipynb** → Importar datos históricos desde múltiples fuentes → `data/processed/`
4. **03_Crowdsourcing_Collection.ipynb** → Recopilación mediante reportes de usuarios → `data/raw/`

**Procesamiento:**

5. **Data_Ingestion_Basic_Procesing.ipynb** → Limpiar/procesar todos los datos → `data/processed/`

**Análisis:**

6. **Realistic_Traffic_Modeling.ipynb** → Modelado y análisis exploratorio → Validación de hipótesis TSI

## Limpieza pendiente

La carpeta `tsi/` está vacía y se puede eliminar cuando no esté bloqueada por VS Code o OneDrive.

Comando (PowerShell):

```powershell
Remove-Item -Path "./tsi" -Recurse -Force
```
