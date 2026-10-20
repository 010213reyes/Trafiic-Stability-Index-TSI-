# 03 Analisis temporal

Estudia la evolucion de las observaciones por fecha, hora y dia de la semana, manteniendo la metrica principal de cada fuente.

## Ejecucion

```powershell
.\.venv\Scripts\python.exe docs\03_analisis_datos\03_analisis_temporal\03_analisis_temporal.py
```

El script procesa el consolidado por lotes y genera salidas locales en `data/03_analysis_output/analisis_temporal/`:

- `cobertura_diaria.csv`;
- `resumen_por_hora.csv`;
- `resumen_por_dia_semana.csv`.

## Resultado inicial

El perfil completo confirma cinco coberturas temporales distintas:

- Istanbul: 3.332 dias observados entre 2015 y 2024, con una observacion diaria.
- Los Angeles County: 119 dias entre marzo y junio de 2012, con cobertura intradia.
- Madrid: 31 dias durante diciembre de 2022, con cobertura intradia.
- San Francisco Bay Area: 181 dias durante el primer semestre de 2017, con cobertura intradia.
- Sao Paulo: 6.094 dias entre 2001 y 2018, con una granularidad diferente a las fuentes de sensores.

## Limitacion

No se deben comparar patrones horarios o tendencias entre fuentes sin normalizar frecuencia, ventana temporal, unidad y disponibilidad. El indicador TSI debe conservar esta diferencia de cobertura como parte de su trazabilidad.
