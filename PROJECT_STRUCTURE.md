# Estructura Organizacional del Proyecto TSI

## Estructura actual

```text
TSI/
├── README.md
├── README_STRUCTURE.md
├── PROJECT_STRUCTURE.md
├── data/
│   ├── 00_raw/
│   ├── 01_processed/
│   ├── 02_clean/
│   └── 03_algorithm_output/
├── notebooks/
│   ├── 01_Data_Collection/
│   ├── 02_Data_Processing/
│   └── 03_Demostracion_Tecnica_TSI/
├── streamlit_dashboard/
└── .venv/
```

## Carpetas principales

### `notebooks/01_Data_Collection/`
Reúne los notebooks de captura y construcción inicial de datos:
`Scraping_Traffic.ipynb`, `01_Synthetic_Traffic_Data.ipynb`, `02_Historical_Data_Import.ipynb`, `03_Crowdsourcing_Collection.ipynb` y `Realistic_Traffic_Modeling.ipynb`.

### `notebooks/02_Data_Processing/`
Contiene el flujo completo de procesamiento y cierre técnico:
`00_Algorithm_Evaluation_Pipeline.ipynb`, `01_Data_Quality_Assessment.ipynb`, `02_Data_Cleaning.ipynb`, `03_Data_Validation.ipynb`, `04_Exploratory_Data_Analysis.ipynb`, `04_Exploratory_Data_Analysis_TSI.ipynb`, `05_Isolation_Forest_TSI.ipynb`, `06_Local_Outlier_Factor_TSI.ipynb`, `07_DBSCAN_TSI.ipynb` y `08_Algorithm_Comparison_and_TSI.ipynb`.

### `notebooks/03_Demostracion_Tecnica_TSI/`
Versión curada para presentación técnica con el notebook `01_Demostracion_Tecnica_TSI.ipynb` y su `README.md`.

### `data/00_raw/`
Datos originales o recién recolectados.

### `data/01_processed/`
Datos intermedios resultantes de transformaciones previas a la validación final.

### `data/02_clean/`
Datos limpios y consolidados, incluidos los datasets filtrados por algoritmo.

### `data/03_algorithm_output/`
Salidas finales de análisis, resúmenes y visualizaciones de los algoritmos.

### `streamlit_dashboard/`
Capa de visualización ejecutiva con `app.py` y `README.md`.

## Flujo recomendado

1. Recolección inicial de datos en `notebooks/01_Data_Collection/`.
2. Limpieza y validación en `notebooks/02_Data_Processing/`.
3. Cierre comparativo y definición del TSI en `08_Algorithm_Comparison_and_TSI.ipynb`.
4. Presentación técnica en `notebooks/03_Demostracion_Tecnica_TSI/`.
5. Visualización ejecutiva en `streamlit_dashboard/`.

## Estado de organización

La estructura ya corresponde al estado final del proyecto y sirve como guía de navegación, documentación y entrega.
   - ¿Existen los datos en `00_raw`?
   - ¿Se ejecutaron los notebooks en orden?
   - ¿Se actualizaron los paths después de mover archivos?

## 🔗 Relación entre Carpetas

```
Recolección → Crudos → Diagnóstico → Limpieza → Validación → Análisis → Insights
    ↓            ↓          ↓          ↓           ↓            ↓         ↓
 01_Data_       00_raw     01_QA      02_Clean    03_Validar  04_EDA   02_clean/
 Collection                                                             insights
```

---
**Última actualización**: 1 de mayo de 2026
**Versión**: 1.0 - Estructura base completada
