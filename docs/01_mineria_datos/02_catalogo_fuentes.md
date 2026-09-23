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

### Selección inicial: 5 ciudades candidatas

Estas cinco ciudades fueron una propuesta inicial basada en similitud urbana y disponibilidad esperada. No todas fueron aprobadas: una ciudad solo entra al conjunto operativo después de verificar una fuente descargable, medible y compatible con el contrato.

| Ciudad | Región | Motivo de selección | Tipo de fuente esperada | Uso previsto |
|---|---|---|---|---|
| Bangkok | Asia | Congestión extrema, clima tropical, altas horas pico, urbano con gran dependencia del transporte privado | Serie de sensores / datos públicos de tránsito | Entrenamiento general de congestión y transferencia temporal |
| Istanbul | Europa-Asia | Megaciudad compleja, patrones de tráfico intensos y red vial heterogénea | Sensores de flujo/velocidad o datos de red urbana | Aprendizaje de patrones de saturación y diversidad de corredores |
| Dubai | Medio Oriente | Expansión urbana rápida, estructura vial moderna, alto volumen de circulación en regiones densas | Datos de tráfico urbano y arterias principales | Transferencia en ciudades con crecimiento rápido y alta demanda |
| Madrid | Europa | Alta calidad de datos abiertos, tráfico urbano medido de forma estructurada | Datos abiertos de tráfico y sensores | Comparación con una ciudad europea con infraestructura observacional sólida |
| Barcelona | Europa | Red urbana compacta, congestión recurrente y mejor disponibilidad de series temporales | Metadatos y series de tránsito públicas | Validación de comportamiento urbano y estabilidad de patrones |

### Estado de la selección inicial

| Ciudad | Estado actual | Motivo |
|---|---|---|
| Bangkok | No aprobada | El portal respondió, pero no se validó un dataset reutilizable de tráfico con la resolución requerida. |
| Istanbul | Aprobada con limitaciones | Existe un índice de tráfico descargado; es agregado y no tiene sensores ni velocidad directa. |
| Dubai | No aprobada | No se obtuvo acceso confiable a un dataset público directamente descargable. |
| Madrid | Aprobada | El Ayuntamiento ofrece históricos oficiales con puntos de medición, intensidad, ocupación y velocidad de fuente. |
| Barcelona | Pendiente, fuera del conjunto actual | El catálogo existe, pero todavía no se identificó una serie operativa compatible con el pipeline. |

### Fuentes internacionales aprobadas para la ingeniería actual

El conjunto operativo cambió respecto de la selección inicial. Se incorporaron Sao Paulo, METR-LA y PEMS-BAY porque tienen evidencia de datos utilizables para las funciones específicas del proyecto.

| Fuente | Ciudad o región | Variable principal | Rol actual | Estado |
|---|---|---|---|---|
| Istanbul Traffic Index | Istanbul | Índice de congestión | Comparación agregada | Raw validado |
| CET Traffic Jams | Sao Paulo | Longitud de congestión | Comparación urbana | Raw y processed validados; copia secundaria del conjunto CET |
| Histórico de puntos de tráfico | Madrid | Intensidad, ocupación y velocidad de fuente | Transferencia urbana | Raw y processed validados |
| METR-LA | Los Angeles County | Velocidad por sensor | Preentrenamiento | Raw y processed validados |
| PEMS-BAY | San Francisco Bay Area | Velocidad por sensor | Transferencia temporal | Raw y processed validados |

Guadalajara permanece como ciudad objetivo de calibración y validación. Las fuentes externas no sustituyen la evidencia local.

### Criterio de compatibilidad

La selección final se basa en cuatro criterios:

1. Cobertura temporal suficiente (al menos 30 días o un periodo continuo equivalente).
2. Resolución útil (5 a 15 minutos).
3. Variables compatibles con el proyecto (velocidad, flujo, ocupación o tiempo de viaje).
4. Estructura de datos que pueda normalizarse a un esquema común sin perder trazabilidad.

### Regla de etiquetado para estas fuentes

Cada observación externa se conservará con etiquetas explícitas para evitar mezclar ciudades o roles de datos. El contrato mínimo incluye:

- `ciudad`
- `pais`
- `fuente`
- `rol_dato` (`entrenamiento`, `calibracion`, `validacion`, `comparacion`)
- `segmento_id`
- `timestamp_local`
- `timezone`
- `es_real`
- `ciudad_objetivo` (`Guadalajara` o `multi_ciudad`)

Esto evita que una ciudad internacional se interprete como Guadalajara o como un dato sintético.

| Fuente candidata | Cobertura conocida | Variables útiles | Resolución | Acceso | Uso previsto |
|---|---|---|---|---|---|
| METR-LA | Los Angeles, 207 sensores, marzo-junio de 2012 | Velocidad | 5 min | Repositorio público | Preentrenamiento y series temporales |
| PEMS-BAY | San Francisco Bay Area, 325 sensores, enero-mayo de 2017 | Velocidad | 5 min | Repositorio público | Preentrenamiento y transferencia |
| Caltrans PeMS | California, red de detectores | Flujo, velocidad, ocupación | 5 min | Cuenta pública gratuita | Fuente primaria y ampliación de variables |
| Madrid tráfico | Madrid, tramos urbanos | Intensidad y nivel de tráfico; confirmar histórico | Variable según conjunto | Portal abierto; posible captura propia | Recolección propia y contraste urbano |
| Bangkok / Istanbul / Dubai / Barcelona | Series públicas o bases observadas locales | Velocidad, flujo, ocupación, congestión | 5-15 min | Variables por disponibilidad | Transferencia internacional y validación multiciudad |

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
