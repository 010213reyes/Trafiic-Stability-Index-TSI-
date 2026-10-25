# 07 Resultados

Esta subfase consolida los resultados reproducibles de las etapas de EDA, calidad, temporalidad, comparacion e indicador provisional.

## Ejecucion

```powershell
.\.venv\Scripts\python.exe docs\03_analisis_datos\07_resultados\07_consolidar_resultados.py
```

Las salidas locales se guardan en `data/03_analysis_output/resultados/`:

- `estado_fase_analisis.json`;
- `hallazgos_por_fuente.csv`.

## Estado actual

- 41.770.880 observaciones evaluadas.
- Cinco grupos ciudad-fuente-metrica.
- Controles basicos de rango sin registros invalidos.
- Comparacion directa candidata solo para METR-LA y PEMS-BAY.
- Indicador TSI provisional, sin mezcla entre fuentes.
- Validacion SQL registrada con `41,770,880` observaciones en MySQL.

## Criterio de cierre

La fase consolida los conteos, controles y hallazgos reproducibles de Parquet junto con la validacion de `tsi_db`.
