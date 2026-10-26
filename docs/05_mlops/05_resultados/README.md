# 05 Resultados

Consolida la ejecucion reproducible, las evidencias, las metricas operativas, los limites y la decision de cierre de la fase MLOps.

## Ejecucion validada

El flujo se ejecuta en dos pasos independientes y una interfaz de consulta:

1. `inferir_tsi.py` carga `rf_tsi_internacional_v1.0.0` desde el registro local y genera predicciones sin reentrenar.
2. `monitorear_flujo.py` calcula controles de calidad, drift descriptivo, desempeño y tasas de anomalia.
3. Streamlit presenta los resultados en `Operacion MLOps` leyendo los archivos generados.

Resultado registrado en los artefactos actuales:

| Evidencia | Resultado |
| --- | ---: |
| Version | `rf_tsi_internacional_v1.0.0` |
| Filas de features | 9,742 |
| Filas inferidas | 9,717 |
| Filas omitidas por features incompletas | 25 |
| MAE de inferencia | 1.7651 |
| RMSE de inferencia | 3.9217 |
| P95 del error absoluto | 7.4593 |
| Drift maximo de media | 0.0258 desviaciones estandar |
| Estado de monitoreo | `ok` |
| Observaciones evaluadas para anomalias | 86,382 |
| Anomalias Isolation Forest | 4,315, aproximadamente 5.00% |

El detalle de cada control y su umbral se conserva en `data/05_mlops/monitoring/reporte_monitoreo.json`.

## Inventario de artefactos

- Registro: `data/05_mlops/model_registry/rf_tsi_internacional_v1.0.0/manifest.json` y `model.joblib`.
- Inferencia: `data/05_mlops/inference/predicciones_tsi.csv` y `predicciones_tsi.json`.
- Monitoreo: `data/05_mlops/monitoring/reporte_monitoreo.json`.
- Anomalias: `data/04_model_output/anomalies/resumen_anomalias.csv`.
- Interfaz: `streamlit_app/app.py`.

## Decision y limites

La fase MLOps se cierra como una demostracion local reproducible: versiona el modelo, fija el hash de entrada, separa inferencia de entrenamiento, conserva metadatos y expone controles operativos en Streamlit.

No se declara despliegue productivo, inferencia en tiempo real ni deteccion universal de pre-colapso. El TSI es provisional y especifico por fuente; las anomalias no tienen ground truth externo; el desempeño depende del objetivo observado disponible; y Guadalajara queda pendiente de calibracion y validacion local.

## Validacion

```powershell
.venv\Scripts\python.exe -m py_compile streamlit_app\app.py
.venv\Scripts\python.exe docs\05_mlops\02_inferencia_reproducible\inferir_tsi.py
.venv\Scripts\python.exe docs\05_mlops\03_monitoreo\monitorear_flujo.py
```
