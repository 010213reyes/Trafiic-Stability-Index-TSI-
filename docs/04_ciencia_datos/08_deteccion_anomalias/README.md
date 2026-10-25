# 08 Deteccion de anomalias

Esta subfase implementa dos detectores exploratorios sobre series de velocidad a 5 minutos:

- baseline estadistico con z-score robusto;
- Isolation Forest con contaminacion configurada en 5%.

El notebook principal es `01_Deteccion_Anomalias_Internacional.ipynb`.

## Artefactos

- `data/04_model_output/anomalies/anomalias_alta_frecuencia.parquet`;
- `data/04_model_output/anomalies/resumen_anomalias.csv`;
- `data/04_model_output/anomalies/resumen_experimento_anomalias.json`.

## Interpretacion

La coincidencia entre ambos metodos mide consistencia interna y sirve para priorizar candidatos. No es precision contra incidentes reales porque METR-LA y PEMS-BAY no incluyen una etiqueta externa sincronizada de accidentes o congestion.
