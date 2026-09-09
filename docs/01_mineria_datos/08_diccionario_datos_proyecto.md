# Diccionario de datos del proyecto punta a punta

Este diccionario pertenece a la implementación nueva del TSI. La investigación inicial conserva sus propios esquemas y resultados; este documento define el contrato común para las fuentes que entren al pipeline nuevo.

## Campos comunes

| Campo | Tipo | Unidad | Obligatorio | Descripción | Regla de calidad |
|---|---|---|---:|---|---|
| `timestamp` | datetime | ISO 8601 | Sí | Momento de la observación | No nulo, ordenable y con zona horaria documentada |
| `ciudad` | string | - | Sí | Ciudad o región de origen | Catálogo controlado |
| `fuente` | string | - | Sí | Dataset, portal o recolector original | No nulo |
| `es_real` | boolean | - | Sí | Distingue observación real de sintética o simulada | `true` para sensores o registros observados |
| `segmento_id` | string | - | Sí | Sensor, tramo o identificador espacial | Único dentro de la fuente |
| `tipo_via` | string | - | Sí | Clasificación de la vía | No mezclar autopista y arterial sin conservar la categoría |
| `latitud` | float | grados | No | Latitud del sensor o segmento | Rango -90 a 90 |
| `longitud` | float | grados | No | Longitud del sensor o segmento | Rango -180 a 180 |
| `velocidad_kmh` | float | km/h | No | Velocidad observada o estimada | Unidad y método deben estar documentados |
| `flujo_veh_h` | float | vehículos/h | No | Volumen de vehículos por hora | No derivar si la fuente no documenta el cálculo |
| `ocupacion_pct` | float | porcentaje | No | Porcentaje de tiempo ocupado del detector | No convertir automáticamente a densidad |
| `densidad_veh_km` | float | vehículos/km | No | Densidad vehicular | Solo si la fuente la mide o documenta su estimación |
| `tiempo_viaje_seg` | float | segundos | No | Tiempo de recorrido del segmento o ruta | Mantener separado de velocidad de sensor |
| `calidad_registro` | string | - | No | Resultado de controles de calidad | `valido`, `advertencia` o `invalido` |

## Mapeo de fuentes actuales

| Fuente | `timestamp` | `segmento_id` | Velocidad | Flujo | Ocupación | Densidad | Estado |
|---|---|---|---|---|---|---|---|
| METR-LA | Primera columna del CSV | Columnas de sensores | Sí | No confirmada | No confirmada | No | Compatible para velocidad |
| PEMS-BAY | Primera columna del CSV | Columnas de sensores | Sí | No confirmada | No confirmada | No | Compatible para velocidad |
| `traffic_data.csv` | `timestamp` | `avenida` | `velocidad` | No disponible | No disponible | `densidad` | Parcial; 310 registros |
| `scraped_traffic.csv` | `timestamp` | `avenida` | `velocidad` | No disponible | No disponible | `densidad` | Parcial; 117 registros |
| `crowdsourcing_raw.csv` | `timestamp` | `road` | `speed_kmh` | No disponible | No disponible | No disponible | Registro de usuarios; 500 observaciones |
| `crowdsourcing_aggregated.csv` | `timestamp` | `road` | `avg_speed` | No disponible | No disponible | No disponible | Agregado; 148 observaciones |
| Guadalajara futura | Por definir | Sensor o segmento | Objetivo | Objetivo | Objetivo | Objetivo | Pendiente de captura |

## Reglas de integración

1. Los archivos de `data/00_raw/` permanecen sin modificar.
2. Los nombres comunes se asignan únicamente en `data/01_processed/`.
3. Las variables ausentes permanecen nulas.
4. No se calcula densidad a partir de velocidad sin una relación documentada.
5. Cada registro conserva ciudad, fuente y segmento.
6. La zona horaria se documenta antes de comparar series temporales.
7. Las autopistas de METR-LA y PEMS-BAY se analizan separadas de las avenidas urbanas de Guadalajara.
8. Las etiquetas de congestión se calculan después de definir una regla por fuente y ciudad.

## Estado del diccionario

El contrato común ya está definido para iniciar la ingeniería de datos. Quedan pendientes la confirmación de unidades y metodología de las variables locales de Guadalajara, así como la incorporación de una fuente real continua de Guadalajara para calibración y validación.