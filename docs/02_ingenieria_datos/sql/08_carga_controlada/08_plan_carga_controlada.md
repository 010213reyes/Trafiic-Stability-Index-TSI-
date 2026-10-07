# SQL-08: plan de carga controlada

## Decisión

El consolidado internacional no se cargará completo en SQLite local. La carga definitiva se ejecutará en **MySQL InnoDB**, leyendo `international_observations.parquet` por grupos y enviando lotes de 250.000 filas.

La decisión evita cargar los 41.770.880 registros en memoria y mantiene separadas la base de prueba SQLite y la base internacional definitiva.

## Plan generado

```powershell
.\.venv\Scripts\python.exe docs\02_ingenieria_datos\sql\08_plan_carga_controlada.py
```

El plan queda en `sql08_controlled_load_plan.json` y actualmente tiene estado `planned_not_executed`.

La entrada tiene 170 grupos Parquet y 41.770.880 filas. Con lotes de 250.000 filas se utilizarán aproximadamente 168 lotes lógicos. El cargador definitivo debe respetar los grupos Parquet, confirmar cada transacción y registrar el resultado en `log_cargas`.

## Orden de carga

1. Ejecutar `08_schema_mysql.sql` para crear el esquema MySQL y sus restricciones.
2. Cargar `dim_ciudad` y `dim_fuente` desde el contrato internacional.
3. Construir `dim_segmento` con la clave compuesta `fuente_id + codigo_segmento`.
4. Leer el consolidado por grupos y cargar `fact_observaciones` por lotes.
5. Registrar filas leídas, insertadas y rechazadas en `log_cargas`.
6. Crear los índices temporales después de cargar los hechos.
7. Ejecutar SQL-09 para validar conteos, rangos, nulos y relaciones.

El cargador preparado es `08_cargar_mysql_lotes.py`. Sin `--execute` funciona en modo de validación y no abre conexión. La ejecución real requiere `mysql-connector-python` y estas variables de entorno: `TSI_MYSQL_HOST`, `TSI_MYSQL_PORT`, `TSI_MYSQL_USER`, `TSI_MYSQL_PASSWORD` y `TSI_MYSQL_DATABASE`.

## Controles obligatorios

- Una transacción por lote.
- Reintento únicamente del lote fallido.
- No insertar credenciales ni contraseñas en scripts o manifiestos.
- Conservar `NULL` en métricas que la fuente no mide.
- Normalizar `tipo_via` ausente como `no_especificado`, igual que en SQL-07.
- No ejecutar la carga completa hasta disponer de una instancia MySQL y credenciales configuradas fuera del repositorio.

## Estado

SQL-08 queda planificado, pero no ejecutado. La ejecución física depende de disponer de MySQL; el siguiente paso técnico es preparar el cargador por lotes y las consultas SQL-09 de validación.