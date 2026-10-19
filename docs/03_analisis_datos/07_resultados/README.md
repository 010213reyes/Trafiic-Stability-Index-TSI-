# 07 Resultados

Esta subfase consolida los resultados reproducibles de las etapas de EDA, calidad, temporalidad, comparacion e indicador provisional.

## Ejecucion

```powershell
.\.venv\Scripts\python.exe scripts\analysis\07_consolidar_resultados.py
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
- Validacion SQL pendiente de completar la carga total en MySQL.

## Criterio de cierre

La fase no se considera completamente cerrada hasta comparar los conteos y agregaciones de Parquet contra `tsi_db`. El resultado actual es analitico y reproducible, pero conserva la dependencia SQL pendiente.
