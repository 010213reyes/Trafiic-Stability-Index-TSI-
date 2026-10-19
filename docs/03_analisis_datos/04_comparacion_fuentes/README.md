# 04 Comparacion de fuentes

Esta subfase establece que fuentes pueden compararse y bajo que condiciones. No convierte metricas distintas en una escala comun sin justificacion.

## Ejecucion

```powershell
.\.venv\Scripts\python.exe scripts\analysis\04_comparacion_fuentes.py
```

Las salidas locales se generan en `data/03_analysis_output/comparacion_fuentes/`:

- `perfil_comparativo_fuentes.csv`;
- `matriz_comparabilidad.csv`.

## Resultado inicial

Se identificaron cinco fuentes y dos candidatas a comparacion directa:

- METR-LA y PEMS-BAY comparten la familia `velocidad_sensor`.
- Istanbul usa `indice_congestion`.
- Madrid usa `intensidad`.
- Sao Paulo usa `congestion_longitud_m`.

Las tres ultimas deben permanecer separadas en su escala original. Las dos fuentes de velocidad requieren verificar unidad, calibracion y ventana temporal antes de comparar valores.

## Regla de interpretacion

Una familia de metrica comun no garantiza comparabilidad estadistica. Toda comparacion debe alinear unidad, periodo, frecuencia, cobertura y poblacion observada.
