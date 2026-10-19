# Arquitectura actual del proyecto

```text
TSI/
├─ data/
│  ├─ 00_raw/external/
│  ├─ 01_processed/
│  └─ 02_clean/
│     ├─ external/
│     └─ consolidated/
├─ docs/
│  ├─ 00_arq_y_decisiones/
│  ├─ 01_mineria_datos/
│  ├─ 02_ingenieria_datos/
│  ├─ 03_analisis_datos/
│  ├─ 04_ciencia_datos/
│  ├─ 05_mlops/
│  └─ 06_interfaz_streamlit/
├─ notebooks/
│  └─ 03_Analisis_Datos/
├─ scripts/
│  ├─ data_pipeline/
│  └─ analysis/
├─ streamlit_dashboard/
├─ .gitignore
└─ README.md
```

## Responsabilidades

- `data/`: almacenamiento por etapas; no contiene logica de negocio.
- `docs/`: decisiones, contratos, modelos, analisis y resultados.
- `scripts/data_pipeline/`: descarga, procesamiento, limpieza y consolidacion de fuentes.
- `scripts/analysis/`: perfiles, controles y resultados analiticos reproducibles.
- `notebooks/03_Analisis_Datos/`: lectura exploratoria y visualizaciones.
- `streamlit_dashboard/`: presentacion de la investigacion internacional.

La carga SQL se mantiene documentada en `docs/02_ingenieria_datos/sql/` y no depende de notebooks legacy.
