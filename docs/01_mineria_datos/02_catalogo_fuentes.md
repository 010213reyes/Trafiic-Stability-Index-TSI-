# Catálogo preliminar de fuentes

Diagnóstico realizado sobre los archivos actuales de `data/00_raw/` y los notebooks de `notebooks/01_Data_Collection/`.

| Fuente | Registros | Días | Cobertura de avenidas | Faltantes | Origen |
|---|---:|---:|---|---|---|
| `traffic_data.csv` | 310 | 9 | 9 nombres de avenida | 222 celdas; principalmente descripción, coordenadas y horario | Base histórica o combinada; requiere confirmar procedencia exacta |
| `synthetic_traffic.csv` | 5,040 | 7 | 5 avenidas | 0 celdas | Generada por `01_Synthetic_Traffic_Data.ipynb` |
| `scraped_traffic.csv` | 117 | 7 | 6 nombres de avenida | 0 celdas | Generada por `Scraping_Traffic.ipynb` |
| `crowdsourcing_raw.csv` | 500 | 30 | 5 avenidas | 0 celdas | Generada por `03_Crowdsourcing_Collection.ipynb` |
| `crowdsourcing_aggregated.csv` | 148 | 30 | 5 avenidas | 15 celdas en `std_speed` | Agregada desde `crowdsourcing_raw.csv` |

## Cobertura temporal observada

- `traffic_data.csv`: 17 de marzo a 1 de mayo de 2026.
- `synthetic_traffic.csv`: 1 a 7 de enero de 2024, con intervalos de 10 minutos.
- `scraped_traffic.csv`: 25 de abril a 1 de mayo de 2026.
- `crowdsourcing_raw.csv`: 29 de marzo a 27 de abril de 2026.
- `crowdsourcing_aggregated.csv`: 29 de marzo a 27 de abril de 2026.

Los periodos no son equivalentes; no deben tratarse como una única serie temporal sin documentar la diferencia.

## Linaje de notebooks

- `01_Synthetic_Traffic_Data.ipynb` genera `synthetic_traffic.csv`.
- `03_Crowdsourcing_Collection.ipynb` genera los dos archivos de crowdsourcing.
- `Scraping_Traffic.ipynb` genera `scraped_traffic.csv` y actualiza `traffic_data.csv`.
- `02_Historical_Data_Import.ipynb` inspecciona y consolida archivos existentes.
- `Realistic_Traffic_Modeling.ipynb` genera una salida en `data/processed/traffic_enriched.csv`, ruta que debe alinearse con la estructura actual.

## Hallazgos de calidad

- No se encontraron filas idénticas repetidas en los cinco archivos mediante comparación textual exacta.
- `traffic_data.csv` tiene faltantes relevantes y nombres de avenida inconsistentes.
- `crowdsourcing_aggregated.csv` tiene faltantes en `std_speed`, probablemente asociados a grupos con una sola observación; debe confirmarse antes de imputar.
- Los esquemas usan nombres diferentes para avenida, velocidad, densidad y detenciones.
- Las unidades deben confirmarse antes de combinar fuentes.

Este catálogo es preliminar y deberá actualizarse con tipos, rangos numéricos, duplicados lógicos y reglas de deduplicación.

## Fuentes públicas multiciudad para transferencia

La falta de una serie pública suficiente de Guadalajara no debe bloquear el aprendizaje de patrones generales. Se buscarán fuentes abiertas de otras ciudades, sin exigir que sean mexicanas, siempre que cumplan el contrato mínimo de datos.

| Fuente candidata | Cobertura conocida | Variables útiles | Resolución | Acceso | Uso previsto |
|---|---|---|---|---|---|
| METR-LA | Los Angeles, 207 sensores, marzo-junio de 2012 | Velocidad | 5 min | Repositorio público | Preentrenamiento y series temporales |
| PEMS-BAY | San Francisco Bay Area, 325 sensores, enero-mayo de 2017 | Velocidad | 5 min | Repositorio público | Preentrenamiento y transferencia |
| Caltrans PeMS | California, red de detectores | Flujo, velocidad, ocupación | 5 min | Cuenta pública gratuita | Fuente primaria y ampliación de variables |
| Madrid tráfico | Madrid, tramos urbanos | Intensidad y nivel de tráfico; confirmar histórico | Variable según conjunto | Portal abierto; posible captura propia | Recolección propia y contraste urbano |

Estas fuentes son observaciones reales de tráfico, pero no son datos reales de Guadalajara. Se conservarán con `ciudad`, `fuente`, `segmento_id` y `es_real` para impedir que se confundan con la evidencia local o con datos sintéticos.

### Contrato mínimo de aceptación

Una fuente externa entra al conjunto de transferencia solo si se verifica:

- origen medido o metodología de medición documentada;
- timestamp y zona horaria identificables;
- resolución de 5 a 15 minutos;
- al menos 30 días o un periodo continuo equivalente;
- varios sensores o segmentos;
- licencia o condiciones de uso compatibles con el proyecto;
- al menos velocidad, o velocidad junto con flujo, ocupación o tiempo de viaje.

No se imputarán densidad, flujo o espera solo para igualar el esquema sintético. Las variables ausentes permanecerán nulas y se usarán únicamente en modelos que no las requieran.

### Estrategia de uso

- Fuentes externas: aprendizaje de patrones generales.
- Guadalajara: calibración y validación local.
- Fuentes sintéticas: pruebas técnicas y control de regresión.

La selección final dependerá de la verificación de descarga, licencia, continuidad y esquema; la ciudad no se elegirá por nacionalidad sino por compatibilidad de datos.
