# Scripts TSI

Los scripts se separan por responsabilidad para evitar mezclar preparación de datos con análisis.

## `data_pipeline/`

Procesa las fuentes internacionales y mantiene el flujo por etapas:

- `download_multicity_traffic_sources.py`: registra y descarga fuentes públicas.
- `process_external_traffic.py`: procesa METR-LA y PEMS-BAY.
- `process_international_sources.py`: normaliza fuentes internacionales.
- `clean_international_sources.py`: genera salidas limpias y controles.
- `consolidate_international_sources.py`: construye el consolidado internacional.

## `analysis/`

Genera perfiles y resultados reproducibles:

- `01_perfil_exploratorio.py`: estructura, nulos y estadisticos.
- `02_calidad_cobertura.py`: calidad, cobertura y rangos.
- `03_analisis_temporal.py`: fechas, horas y dias de semana.
- `04_comparacion_fuentes.py`: matriz de comparabilidad.
- `05_indicador_tsi_provisional.py`: componente TSI provisional.
- `06_validacion_sql.py`: comparacion Parquet contra MySQL.
- `07_consolidar_resultados.py`: estado consolidado de la fase.

## `modeling/`

Reservada para construccion de caracteristicas, particiones temporales, entrenamiento y evaluacion. Permanece sin experimentos hasta cerrar la definicion de etiqueta y la validacion de datos.

Todos los scripts calculan la raiz del proyecto desde su propia ubicacion y deben ejecutarse desde la raiz de TSI.
