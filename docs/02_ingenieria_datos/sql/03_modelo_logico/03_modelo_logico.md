# SQL-03: modelo lógico

## Objetivo

Convertir el modelo conceptual en tablas lógicas, definiendo identificadores, claves y relaciones sin entrar todavía en tipos específicos de MySQL.

## Esquema lógico general

```text
dim_ciudad
    1
    |
    +---------------------- N dim_fuente
    |                           |
    |                           +---------------- N dim_segmento
    |                                                     |
    +---------------------- N fact_observaciones ----------+
                                                                  |
                                                                  +--- N calidad_observacion

fact_agregado
    N ---------------------- 1 dim_ciudad
    N ---------------------- 1 dim_fuente
    N ---------------------- 1 dim_segmento (opcional)
```

## `dim_ciudad`

| Campo lógico | Clave | Obligatorio | Descripción |
|---|---|---:|---|
| `ciudad_id` | PK | Sí | Identificador interno |
| `nombre` | UK | Sí | Nombre controlado |
| `pais` | - | Sí | País de origen |
| `region` | - | No | Región geográfica |
| `zona_horaria` | - | Sí | Zona horaria documentada |
| `es_ciudad_objetivo` | - | Sí | Identifica Guadalajara |

La clave única `nombre + pais` evita duplicar una ciudad.

## `dim_fuente`

| Campo lógico | Clave | Obligatorio | Descripción |
|---|---|---:|---|
| `fuente_id` | PK | Sí | Identificador interno |
| `ciudad_id` | FK | Sí | Ciudad asociada |
| `nombre` | UK dentro de ciudad | Sí | Nombre de la fuente |
| `tipo_fuente` | - | Sí | Sensor, índice, CET, sintética, etc. |
| `origen_url` | - | No | URL de procedencia |
| `licencia` | - | No | Condiciones conocidas |
| `rol_dato` | - | Sí | Transferencia, comparación, calibración o validación |
| `es_real` | - | Sí | Real o sintética |
| `fecha_inicio` | - | No | Inicio documentado |
| `fecha_fin` | - | No | Fin documentado |
| `frecuencia_documentada` | - | No | Resolución conocida |

## `dim_segmento`

| Campo lógico | Clave | Obligatorio | Descripción |
|---|---|---:|---|
| `segmento_id` | PK | Sí | Identificador interno |
| `ciudad_id` | FK | Sí | Ciudad del segmento |
| `fuente_id` | FK | Sí | Fuente que define el código |
| `codigo_segmento` | UK compuesta | Sí | Código original del sensor o tramo |
| `nombre_segmento` | - | No | Avenida, passage o segmento |
| `tipo_via` | - | Sí | Urbana, autopista, M30, agregado, etc. |
| `latitud` | - | No | Ubicación si existe |
| `longitud` | - | No | Ubicación si existe |

La clave única recomendada es `fuente_id + codigo_segmento`, porque un código puede repetirse entre fuentes.

## `fact_observaciones`

Es la tabla central. Cada fila representa una medición en un momento y segmento.

| Campo lógico | Clave | Obligatorio | Descripción |
|---|---|---:|---|
| `observacion_id` | PK | Sí | Identificador único |
| `timestamp` | - | Sí | Momento normalizado |
| `ciudad_id` | FK | Sí | Ciudad de la observación |
| `fuente_id` | FK | Sí | Procedencia |
| `segmento_id` | FK | Sí | Sensor, tramo o agregado |
| `metrica_principal` | - | Sí | Tipo de métrica principal |
| `valor_principal` | - | Sí | Valor de la métrica principal |
| `velocidad_kmh` | - | No | Velocidad confirmada |
| `flujo_veh_h` | - | No | Flujo o intensidad mapeada |
| `ocupacion_pct` | - | No | Ocupación del detector |
| `densidad_veh_km` | - | No | Densidad documentada |
| `tiempo_viaje_seg` | - | No | Tiempo de viaje |
| `congestion_longitud_m` | - | No | Longitud de congestión de São Paulo |
| `indice_congestion` | - | No | Índice agregado de Istanbul |
| `intensidad_fuente` | - | No | Intensidad original de Madrid |
| `carga_fuente` | - | No | Carga original de Madrid |
| `vmed_fuente` | - | No | Velocidad original de Madrid |
| `calidad_registro` | - | Sí | Válido o advertencia |

Las columnas métricas pueden ser nulas. No se rellenan artificialmente.

## `calidad_observacion`

| Campo lógico | Clave | Obligatorio | Descripción |
|---|---|---:|---|
| `calidad_id` | PK | Sí | Identificador del hallazgo |
| `observacion_id` | FK | Sí | Observación relacionada |
| `tipo_problema` | - | Sí | Nulo, rango, unidad, continuidad, etc. |
| `descripcion` | - | Sí | Explicación |
| `severidad` | - | Sí | Informativa, advertencia o invalida |
| `fecha_revision` | - | Sí | Fecha de revisión |

Esta tabla puede quedar vacía si solo se conserva `calidad_registro`.

## `fact_agregado`

| Campo lógico | Clave | Obligatorio | Descripción |
|---|---|---:|---|
| `agregado_id` | PK | Sí | Identificador del resumen |
| `ciudad_id` | FK | Sí | Ciudad resumida |
| `fuente_id` | FK | Sí | Fuente resumida |
| `segmento_id` | FK | No | Segmento si aplica |
| `periodo_inicio` | - | Sí | Inicio del periodo |
| `periodo_fin` | - | Sí | Fin del periodo |
| `metrica` | - | Sí | Métrica resumida |
| `valor_agregado` | - | Sí | Valor calculado |
| `cantidad_observaciones` | - | Sí | Registros utilizados |

## Relaciones y cardinalidades

```text
dim_ciudad 1 ---- N dim_fuente
dim_ciudad 1 ---- N dim_segmento
dim_fuente 1 ---- N dim_segmento
dim_ciudad 1 ---- N fact_observaciones
dim_fuente 1 ---- N fact_observaciones
dim_segmento 1 -- N fact_observaciones
fact_observaciones 1 ---- N calidad_observacion
dim_ciudad 1 ---- N fact_agregado
dim_fuente 1 ---- N fact_agregado
dim_segmento 1 -- N fact_agregado (opcional)
```

## Decisiones de alcance

- No se crea una tabla por ciudad.
- No se crea una tabla por métrica.
- No se crea una tabla de usuarios.
- No se cargan imágenes ni notebooks.
- Los resultados de Isolation Forest, LOF y DBSCAN quedan fuera de `fact_observaciones`.
- Podrán tener una tabla propia en la fase de análisis si se necesita consultar anomalías.

## Criterio de aprobación

Este modelo queda listo para revisión en papel. Después seguirá SQL-04, donde se fijará la representación definitiva de las métricas antes de asignar tipos MySQL.