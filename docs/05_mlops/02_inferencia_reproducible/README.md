# 02 Inferencia reproducible

Define una ejecución separada del entrenamiento para recibir datos válidos, cargar el modelo versionado y producir predicciones, TSI y señales de anomalía.

## Entregables

- script o módulo de inferencia;
- contrato de entrada y salida;
- validaciones de esquema y tipos;
- artefactos de resultados con metadatos de ejecución.

## Ejecución

Desde la raíz del proyecto:

```powershell
.venv\Scripts\python.exe docs\05_mlops\02_inferencia_reproducible\inferir_tsi.py
```

También puede recibir otro archivo compatible:

```powershell
.venv\Scripts\python.exe docs\05_mlops\02_inferencia_reproducible\inferir_tsi.py --input ruta\entrada.parquet --output ruta\salida.csv
```

La inferencia conserva las filas con features completas, genera `prediccion_tsi_siguiente` y, cuando existe el objetivo observado, calcula `error_absoluto`. El archivo JSON contiguo registra la versión del modelo y el hash de entrada.
