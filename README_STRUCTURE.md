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
├─ streamlit_app/
├─ .gitignore
└─ README.md
```

## Responsabilidades

- `data/`: almacenamiento por etapas; no contiene logica de negocio.
- `docs/`: decisiones, contratos, modelos, analisis y resultados.
- `docs/02_ingenieria_datos/`: scripts de descarga, procesamiento, consolidacion y SQL dentro de cada subfase.
- `docs/03_analisis_datos/`: scripts, notebook, salidas y documentacion de cada subfase analitica.
- `streamlit_app/`: aplicacion Streamlit de la investigacion internacional.

La carga SQL se mantiene documentada en `docs/02_ingenieria_datos/sql/` y no depende de notebooks legacy.
