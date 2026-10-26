# 04 Integracion de la demostracion

Conecta los artefactos aprobados de MLOps con Streamlit sin trasladar entrenamiento, limpieza ni logica de versionado al codigo de presentacion.

## Contrato de lectura

La pestaña `Operacion MLOps` lee los siguientes artefactos relativos a la raiz del proyecto:

| Artefacto | Uso en la interfaz |
| --- | --- |
| `data/05_mlops/model_registry/rf_tsi_internacional_v1.0.0/manifest.json` | Version, parametros, predictores, filas de entrenamiento y metricas de evaluacion |
| `data/05_mlops/inference/predicciones_tsi.json` | Fecha de ejecucion, hash de entrada y filas procesadas u omitidas |
| `data/05_mlops/inference/predicciones_tsi.csv` | Predicciones, objetivo observado y error absoluto |
| `data/05_mlops/monitoring/reporte_monitoreo.json` | Estado, desempeño, drift, nulos, rango del TSI y tasas de anomalia |
| `data/04_model_output/anomalies/resumen_anomalias.csv` | Resumen exploratorio por fuente |

La interfaz muestra una advertencia si faltan los artefactos principales. No reentrena el modelo, no recalcula el TSI y no modifica datos RAW, CLEAN ni los resultados publicados.

## Ejecucion local

Desde la raiz del proyecto:

```powershell
.venv\Scripts\python.exe docs\05_mlops\02_inferencia_reproducible\inferir_tsi.py
.venv\Scripts\python.exe docs\05_mlops\03_monitoreo\monitorear_flujo.py
.venv\Scripts\python.exe -m streamlit run streamlit_app\app.py
```

La aplicacion solicita el acceso de demostracion configurado en `streamlit_app/app.py`. La vista se considera operativa cuando muestra la version `rf_tsi_internacional_v1.0.0`, predicciones, metricas y controles de monitoreo.

## Evidencia de salud

La ejecucion validada del servidor local respondio `HTTP 200` en la ruta de salud de Streamlit. La validacion de sintaxis se realiza con:

```powershell
.venv\Scripts\python.exe -m py_compile streamlit_app\app.py
```

La interfaz es una demostracion operativa local; no representa un despliegue productivo ni un sistema de observabilidad en tiempo real.
