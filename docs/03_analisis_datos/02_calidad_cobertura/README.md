# 02 Calidad y cobertura

Esta subfase evalua completitud, cobertura temporal, etiquetas de calidad y rangos plausibles del consolidado internacional.

## Ejecucion

```powershell
.\.venv\Scripts\python.exe docs\03_analisis_datos\02_calidad_cobertura\02_calidad_cobertura.py
```

El script procesa el Parquet por lotes y genera salidas locales en `data/03_analysis_output/calidad_cobertura/`:

- `calidad_global.json`;
- `cobertura_por_fuente.csv`;
- `etiquetas_por_fuente.csv`;
- `controles_de_rango.csv`.

## Resultado inicial

El perfil completo cubre 41.770.880 observaciones y cinco grupos ciudad-fuente-metrica.

- No se detectaron timestamps invalidos.
- No se detectaron valores principales negativos.
- No se detectaron periodos de integracion no positivos.
- No se detectaron coordenadas fuera de rango entre las coordenadas informadas.
- Los faltantes de coordenadas, `valor_fuente`, `periodo_integracion_min` y `tipo_via` se reportan por fuente y no se consideran automaticamente errores, porque dependen de la naturaleza de cada proveedor.

## Limitacion

La cobertura temporal no es equivalente entre fuentes. Las comparaciones internacionales deben controlar periodo, frecuencia, unidad y disponibilidad antes de calcular indicadores comunes.
