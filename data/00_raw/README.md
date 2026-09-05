# Fuentes de datos raw

Esta carpeta contiene los datos originales o generados en la etapa de recolección. Los archivos no deben sobrescribirse durante la limpieza o el modelado. Las transformaciones deben producir salidas en `data/01_processed/`, `data/02_clean/` o `data/03_algorithm_output/`.

## Inventario actual

| Archivo | Tipo de fuente | Variables principales observadas | Uso inicial | Riesgos o limitaciones |
|---|---|---|---|---|
| `traffic_data.csv` | Histórica/base | `timestamp`, `avenida`, `velocidad`, `densidad`, `detenciones`, ubicación y horario | Punto de partida para tráfico observado | Tiene pocas columnas operativas y cobertura limitada; debe revisarse su origen exacto |
| `synthetic_traffic.csv` | Sintética | `timestamp`, `road`, `hour`, `velocity_kmh`, `density_veh_km`, `flow_veh_h`, `wait_time_sec`, `stops_count` | Pruebas de estructura, relaciones y pipeline | No representa observaciones reales; puede contener patrones definidos por el generador |
| `scraped_traffic.csv` | Scraping | `timestamp`, `avenida`, `latitud`, `longitud`, `velocidad`, `densidad`, `detenciones`, `horario`, `descripcion` | Ampliar observaciones de tráfico | Dependencia de la fuente consultada, fecha de captura y reglas de scraping |
| `crowdsourcing_raw.csv` | Crowdsourcing | Usuario, tiempo, avenida, ubicación, velocidad, tipo de reporte, confianza y dispositivo | Analizar reportes individuales | Sesgo de participación, usuarios repetidos, cobertura irregular y confianza variable |
| `crowdsourcing_aggregated.csv` | Derivada de crowdsourcing | Tiempo, avenida, velocidades agregadas, confianza, reportes y usuarios únicos | Consultas resumidas por periodo y avenida | Es un agregado, no debe confundirse con una fuente independiente |

## Linaje conocido

- `01_Synthetic_Traffic_Data.ipynb` genera `synthetic_traffic.csv`.
- `03_Crowdsourcing_Collection.ipynb` genera `crowdsourcing_raw.csv` y `crowdsourcing_aggregated.csv`.
- `Scraping_Traffic.ipynb` genera `scraped_traffic.csv` y también trabaja con `traffic_data.csv`.
- `02_Historical_Data_Import.ipynb` inspecciona y consolida las fuentes existentes.
- `Realistic_Traffic_Modeling.ipynb` genera datos simulados para modelado realista; debe confirmarse qué archivo utiliza como salida final.

## Diferencias de esquema

Las fuentes no comparten nombres ni unidades completamente uniformes:

- `avenida` y `road` representan la vía, pero requieren un nombre estándar.
- `velocidad`, `velocity_kmh` y `speed_kmh` representan velocidad con nombres distintos.
- `densidad` y `density_veh_km` requieren confirmar unidad y significado.
- `detenciones` y `stops_count` parecen relacionados, pero deben validarse antes de combinarlos.
- Las coordenadas aparecen con nombres y disponibilidad variable.
- Los timestamps deben normalizarse a una zona horaria y formato comunes.

No se deben unir estas fuentes directamente hasta definir un diccionario de datos y reglas de normalización.

## Observaciones de calidad inicial

El inventario debe confirmarse con un diagnóstico reproducible de:

- Número de registros por archivo.
- Número y tipo de columnas.
- Valores nulos y duplicados.
- Rango temporal.
- Cobertura por avenida.
- Unidades y rangos plausibles.
- Repetición de usuarios o registros.
- Consistencia de coordenadas.

Este README documenta lo observado en los encabezados y en los notebooks de recolección; no sustituye el diagnóstico formal de la Fase 1.

## Regla de uso

`00_raw` es una zona de entrada y conservación. La limpieza, integración, imputación, estandarización y generación de variables deben documentarse y ejecutarse fuera de esta carpeta.

## Próximo documento recomendado

El siguiente entregable de minería de datos debe ser `docs/01_mineria_datos/02_catalogo_fuentes.md`, con conteos, rangos, cobertura y evidencia concreta de cada archivo.
