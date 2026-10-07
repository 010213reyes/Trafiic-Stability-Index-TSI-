# SQL-05: modelo físico para MySQL

## Objetivo

Asignar tipos, restricciones e índices al modelo lógico aprobado, preparando el diseño para el diagrama EER de MySQL Workbench. Este documento todavía no contiene sentencias `CREATE TABLE`.

## Convenciones generales

- Motor: InnoDB.
- Juego de caracteres: `utf8mb4`.
- Fechas de observación: `DATETIME(6)` almacenado en UTC.
- Identificadores internos: `BIGINT UNSIGNED AUTO_INCREMENT` para hechos y `INT UNSIGNED AUTO_INCREMENT` para dimensiones.
- Métricas observadas: `DOUBLE`, porque provienen de fuentes heterogéneas y algunas unidades están pendientes de confirmación.
- Banderas: `BOOLEAN`.
- Campos de texto controlado: `VARCHAR` con límites explícitos.
- URLs y notas extensas: `TEXT`.

## `dim_ciudad`

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `ciudad_id` | `INT UNSIGNED` | No | PK, autoincremental |
| `nombre` | `VARCHAR(100)` | No | Parte de UK con `pais` |
| `pais` | `VARCHAR(100)` | No | Parte de UK con `nombre` |
| `region` | `VARCHAR(100)` | Sí | - |
| `zona_horaria` | `VARCHAR(64)` | No | - |
| `es_ciudad_objetivo` | `BOOLEAN` | No | Default `FALSE` |

Índice: `UNIQUE(nombre, pais)`.

## `dim_fuente`

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `fuente_id` | `INT UNSIGNED` | No | PK, autoincremental |
| `ciudad_id` | `INT UNSIGNED` | No | FK a `dim_ciudad` |
| `nombre` | `VARCHAR(150)` | No | UK con `ciudad_id` |
| `tipo_fuente` | `VARCHAR(50)` | No | - |
| `origen_url` | `TEXT` | Sí | - |
| `licencia` | `VARCHAR(255)` | Sí | - |
| `rol_dato` | `VARCHAR(40)` | No | - |
| `es_real` | `BOOLEAN` | No | - |
| `fecha_inicio` | `DATE` | Sí | - |
| `fecha_fin` | `DATE` | Sí | - |
| `frecuencia_documentada` | `VARCHAR(30)` | Sí | - |

Índices: FK `ciudad_id`, `UNIQUE(ciudad_id, nombre)`.

## `dim_segmento`

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `segmento_id` | `BIGINT UNSIGNED` | No | PK, autoincremental |
| `ciudad_id` | `INT UNSIGNED` | No | FK a `dim_ciudad` |
| `fuente_id` | `INT UNSIGNED` | No | FK a `dim_fuente` |
| `codigo_segmento` | `VARCHAR(150)` | No | UK con `fuente_id` |
| `nombre_segmento` | `VARCHAR(255)` | Sí | - |
| `tipo_via` | `VARCHAR(50)` | No | - |
| `latitud` | `DOUBLE` | Sí | CHECK entre -90 y 90 |
| `longitud` | `DOUBLE` | Sí | CHECK entre -180 y 180 |

Índices: FKs y `UNIQUE(fuente_id, codigo_segmento)`.

## `fact_observaciones`

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `observacion_id` | `BIGINT UNSIGNED` | No | PK, autoincremental |
| `timestamp` | `DATETIME(6)` | No | UTC |
| `ciudad_id` | `INT UNSIGNED` | No | FK a `dim_ciudad` |
| `fuente_id` | `INT UNSIGNED` | No | FK a `dim_fuente` |
| `segmento_id` | `BIGINT UNSIGNED` | No | FK a `dim_segmento` |
| `metrica_principal` | `VARCHAR(50)` | No | - |
| `valor_principal` | `DOUBLE` | No | - |
| `velocidad_kmh` | `DOUBLE` | Sí | No inventar valores |
| `flujo_veh_h` | `DOUBLE` | Sí | Unidad pendiente en Madrid |
| `ocupacion_pct` | `DOUBLE` | Sí | CHECK entre 0 y 100 si aplica |
| `densidad_veh_km` | `DOUBLE` | Sí | - |
| `tiempo_viaje_seg` | `DOUBLE` | Sí | CHECK no negativo |
| `congestion_longitud_m` | `DOUBLE` | Sí | CHECK no negativo |
| `indice_congestion` | `DOUBLE` | Sí | Rango según fuente |
| `intensidad_fuente` | `DOUBLE` | Sí | Valor original |
| `carga_fuente` | `DOUBLE` | Sí | Valor original |
| `vmed_fuente` | `DOUBLE` | Sí | Unidad pendiente |
| `calidad_registro` | `VARCHAR(20)` | No | `valido` o `advertencia` |

Índices iniciales:

- `(timestamp)` para consultas temporales;
- `(ciudad_id, timestamp)` para series por ciudad;
- `(fuente_id, timestamp)` para cobertura por fuente;
- `(segmento_id, timestamp)` para series por segmento;
- `(metrica_principal, timestamp)` para familias de métricas.

No se crea una restricción única sobre timestamp, ciudad y segmento hasta verificar que todas las fuentes respeten esa granularidad.

## `calidad_observacion`

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `calidad_id` | `BIGINT UNSIGNED` | No | PK, autoincremental |
| `observacion_id` | `BIGINT UNSIGNED` | No | FK a `fact_observaciones` |
| `tipo_problema` | `VARCHAR(50)` | No | - |
| `descripcion` | `TEXT` | No | - |
| `severidad` | `VARCHAR(20)` | No | - |
| `fecha_revision` | `DATETIME(6)` | No | - |

Índice: `(observacion_id)`.

## `fact_agregado`

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `agregado_id` | `BIGINT UNSIGNED` | No | PK, autoincremental |
| `ciudad_id` | `INT UNSIGNED` | No | FK a `dim_ciudad` |
| `fuente_id` | `INT UNSIGNED` | No | FK a `dim_fuente` |
| `segmento_id` | `BIGINT UNSIGNED` | Sí | FK a `dim_segmento` |
| `periodo_inicio` | `DATETIME(6)` | No | - |
| `periodo_fin` | `DATETIME(6)` | No | - |
| `metrica` | `VARCHAR(50)` | No | - |
| `valor_agregado` | `DOUBLE` | No | - |
| `cantidad_observaciones` | `INT UNSIGNED` | No | - |

Índices: `(ciudad_id, periodo_inicio)`, `(fuente_id, periodo_inicio)` y `(segmento_id, periodo_inicio)`.

## `log_cargas`

Tabla de trazabilidad de importaciones, no de usuarios de la interfaz.

| Campo | Tipo MySQL | Nulo | Restricción |
|---|---|---:|---|
| `carga_id` | `BIGINT UNSIGNED` | No | PK, autoincremental |
| `fuente_id` | `INT UNSIGNED` | Sí | FK a `dim_fuente` |
| `archivo_origen` | `VARCHAR(500)` | No | - |
| `fecha_inicio` | `DATETIME(6)` | No | - |
| `fecha_fin` | `DATETIME(6)` | Sí | - |
| `filas_leidas` | `BIGINT UNSIGNED` | No | Default 0 |
| `filas_insertadas` | `BIGINT UNSIGNED` | No | Default 0 |
| `filas_rechazadas` | `BIGINT UNSIGNED` | No | Default 0 |
| `estado` | `VARCHAR(20)` | No | iniciada, completada o error |
| `mensaje` | `TEXT` | Sí | - |

## Orden de creación

```text
dim_ciudad
    ↓
dim_fuente
    ↓
dim_segmento
    ↓
fact_observaciones
    ↓
calidad_observacion y fact_agregado
    ↓
log_cargas
```

## Decisiones no incluidas

- No se incluyen `usuarios`, `roles` ni `sesiones`; pertenecen a la interfaz.
- No se crean índices sobre cada columna métrica; aumentaría el costo de carga sin una consulta definida.
- No se usa `ENUM` para ciudades, fuentes o métricas; se conservará flexibilidad para nuevas ciudades.
- No se carga todavía el consolidado de 41.7 millones de filas.

## Criterio de aprobación

SQL-05 queda listo para revisión cuando se confirme que los tipos, claves e índices representan el modelo lógico y no contradicen la política de métricas. El siguiente paso será SQL-06: dibujar el modelo EER en MySQL Workbench.