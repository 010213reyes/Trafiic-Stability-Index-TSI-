# Estructura del proyecto (TSI)

Este documento resume cómo está organizado actualmente el proyecto desde la raíz.

## Árbol de carpetas

```text
TSI/
├─ README.md
├─ README_STRUCTURE.md
├─ data/
│  ├─ 00_raw/
│  ├─ 01_processed/
│  ├─ 02_clean/
│  └─ 03_algorithm_output/
├─ notebooks/
│  ├─ 01_Data_Collection/
│  │  ├─ 01_Synthetic_Traffic_Data.ipynb
│  │  ├─ 02_Historical_Data_Import.ipynb
│  │  ├─ 03_Crowdsourcing_Collection.ipynb
│  │  ├─ Realistic_Traffic_Modeling.ipynb
│  │  └─ Scraping_Traffic.ipynb
│  ├─ 02_Data_Processing/
│  │  ├─ 00_Algorithm_Evaluation_Pipeline.ipynb
│  │  ├─ 01_Data_Quality_Assessment.ipynb
│  │  ├─ 02_Data_Cleaning.ipynb
│  │  ├─ 03_Data_Validation.ipynb
│  │  ├─ 04_Exploratory_Data_Analysis.ipynb
│  │  ├─ 04_Exploratory_Data_Analysis_TSI.ipynb
│  │  ├─ 05_Isolation_Forest_TSI.ipynb
│  │  ├─ 06_Local_Outlier_Factor_TSI.ipynb
│  │  ├─ 07_DBSCAN_TSI.ipynb
│  │  └─ 08_Algorithm_Comparison_and_TSI.ipynb
│  └─ 03_Demostracion_Tecnica_TSI/
│     ├─ README.md
│     └─ 01_Demostracion_Tecnica_TSI.ipynb
├─ streamlit_dashboard/
│  ├─ README.md
│  └─ app.py
├─ .venv/
├─ .gitignore
└─ README_STRUCTURE.md
```

## Qué va en cada carpeta

- `data/00_raw/`: datos originales o recién recolectados.
- `data/01_processed/`: etapa intermedia de preparación.
- `data/02_clean/`: datos limpios y consolidados listos para análisis.
- `data/03_algorithm_output/`: salidas gráficas y resúmenes de algoritmos.
- `notebooks/01_Data_Collection/`: notebooks de captura y generación de datos.
- `notebooks/02_Data_Processing/`: notebooks de limpieza, validación, EDA y cierre de TSI.
- `notebooks/03_Demostracion_Tecnica_TSI/`: versión curada para presentación técnica.
- `streamlit_dashboard/`: capa separada para visualización ejecutiva y dashboards.
- `.venv/`: entorno virtual local de Python.

## Flujo recomendado (Pipeline del proyecto)

**Recopilación y construcción de datos:**

1. **Scraping_Traffic.ipynb** → Web scraping de fuentes públicas → `data/00_raw/`
2. **01_Synthetic_Traffic_Data.ipynb** → Generación de datos sintéticos realistas → `data/00_raw/`
3. **02_Historical_Data_Import.ipynb** → Importar datos históricos desde múltiples fuentes → `data/00_raw/`
4. **03_Crowdsourcing_Collection.ipynb** → Recopilación mediante reportes de usuarios → `data/00_raw/`

**Procesamiento:**

5. **Data_Ingestion_Basic_Procesing.ipynb** → Limpiar/procesar todos los datos → `data/01_processed/` y `data/02_clean/`
6. **01_Data_Quality_Assessment.ipynb** → Diagnóstico de calidad
7. **02_Data_Cleaning.ipynb** → Limpieza y normalización
8. **03_Data_Validation.ipynb** → Validación posterior a limpieza
9. **04_Exploratory_Data_Analysis_TSI.ipynb** → EDA consolidado del sistema
10. **05_Isolation_Forest_TSI.ipynb** → Filtrado por Isolation Forest
11. **06_Local_Outlier_Factor_TSI.ipynb** → Filtrado por LOF
12. **07_DBSCAN_TSI.ipynb** → Filtrado y segmentación por DBSCAN
13. **08_Algorithm_Comparison_and_TSI.ipynb** → Comparación final y cierre del TSI

**Presentación ejecutiva:**

14. **03_Demostracion_Tecnica_TSI/** → Demostración técnica curada
15. **streamlit_dashboard/** → Visualización resumida de resultados y decisión final

## Estado

La estructura documentada corresponde al estado actual del repositorio y sirve como referencia para navegación y entrega.
