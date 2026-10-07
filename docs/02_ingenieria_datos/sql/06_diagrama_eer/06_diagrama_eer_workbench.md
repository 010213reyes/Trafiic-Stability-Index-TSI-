# SQL-06: diagrama EER y guía para MySQL Workbench

## Objetivo

Construir visualmente el modelo físico de la base TSI antes de crear tablas definitivas o cargar los 41.7 millones de observaciones.

## Distribución visual recomendada

Coloca las tablas en este orden para que las relaciones se lean de izquierda a derecha:

```text
+-------------+       +-------------+       +---------------+
| dim_ciudad  | 1   N | dim_fuente  | 1   N | dim_segmento  |
+-------------+-------+-------------+-------+---------------+
        |                      |                     |
        | 1                    | 1                   | 1
        |                      |                     |
        +----------------------+---------------------+
                               |
                               N
                    +------------------------+
                    | fact_observaciones     |
                    +------------------------+
                               |
                               | 1
                               |
                               N
                    +------------------------+
                    | calidad_observacion    |
                    +------------------------+

                    +------------------------+
                    | fact_agregado          |
                    +------------------------+

                    +------------------------+
                    | log_cargas             |
                    +------------------------+
```

`fact_agregado` se relaciona con ciudad, fuente y opcionalmente segmento. `log_cargas` se relaciona con `dim_fuente` mediante `fuente_id`.

## Tablas que deben aparecer en el diagrama

1. `dim_ciudad`
2. `dim_fuente`
3. `dim_segmento`
4. `fact_observaciones`
5. `calidad_observacion`
6. `fact_agregado`
7. `log_cargas`

No agregues `usuarios`, `roles` ni `sesiones` en este diagrama. Esas tablas pertenecen a la futura capa de aplicación Streamlit.

## Relaciones que deben dibujarse

```text
dim_ciudad.ciudad_id
    1 ---- N dim_fuente.ciudad_id

dim_ciudad.ciudad_id
    1 ---- N dim_segmento.ciudad_id

dim_fuente.fuente_id
    1 ---- N dim_segmento.fuente_id

dim_ciudad.ciudad_id
    1 ---- N fact_observaciones.ciudad_id

dim_fuente.fuente_id
    1 ---- N fact_observaciones.fuente_id

dim_segmento.segmento_id
    1 ---- N fact_observaciones.segmento_id

fact_observaciones.observacion_id
    1 ---- N calidad_observacion.observacion_id

dim_ciudad.ciudad_id
    1 ---- N fact_agregado.ciudad_id

dim_fuente.fuente_id
    1 ---- N fact_agregado.fuente_id

dim_segmento.segmento_id
    1 ---- N fact_agregado.segmento_id (opcional)

dim_fuente.fuente_id
    1 ---- N log_cargas.fuente_id (opcional)
```

## Guía de construcción en MySQL Workbench

### Paso 1. Crear un modelo nuevo

1. Abrir MySQL Workbench.
2. Seleccionar `File > New Model`.
3. En `Model Overview`, abrir `Add Diagram`.
4. Crear un diagrama EER vacío.

### Paso 2. Crear las tablas

1. Seleccionar la herramienta `Place a New Table`.
2. Crear cada tabla con el nombre exacto de la lista.
3. Agregar primero las columnas identificadoras.
4. Marcar como `PK` las claves primarias.
5. Marcar como `NN` los campos obligatorios.
6. Agregar las columnas restantes según `05_modelo_fisico_mysql.md`.

### Paso 3. Crear relaciones

1. Usar la herramienta `1:n Non-Identifying Relationship`.
2. Seleccionar primero la tabla padre.
3. Seleccionar después la tabla hija.
4. Confirmar que Workbench cree la FK en la tabla hija.
5. Repetir las relaciones de esta guía.
6. Usar relación no identificadora porque las tablas hijas tienen su propia clave primaria.

### Paso 4. Ordenar el diagrama

Coloca:

- `dim_ciudad`, `dim_fuente` y `dim_segmento` en la parte superior;
- `fact_observaciones` en el centro;
- `calidad_observacion` debajo de observaciones;
- `fact_agregado` a la derecha o debajo;
- `log_cargas` junto a `dim_fuente`.

El diagrama debe poder leerse sin líneas cruzadas innecesarias.

### Paso 5. Revisar antes de exportar

Comprobar:

- todas las tablas tienen PK;
- todas las FKs apuntan a la tabla correcta;
- `fact_observaciones` no tiene una tabla de métricas separada;
- `log_cargas` no contiene usuarios;
- no existen tablas por ciudad;
- las métricas pueden ser nulas;
- Istanbul conserva su segmento agregado;
- Madrid conserva sus columnas `_fuente`.

### Paso 6. Guardar el modelo

Guardar el archivo de Workbench como:

```text
docs/02_ingenieria_datos/sql/06_diagrama_eer/tsi_modelo_fisico.mwb
```

El archivo `.mwb` no debe sustituir la documentación en Markdown ni los Parquet de datos.

## No ejecutar todavía

En esta subfase todavía no se debe:

- ejecutar `CREATE TABLE` en producción;
- cargar el consolidado completo;
- crear usuarios de la aplicación;
- crear índices adicionales sin una consulta definida;
- conectar Streamlit a esta base definitiva.

## Criterio de aprobación

SQL-06 queda aprobado cuando el diagrama visual tenga las siete tablas, las relaciones indicadas y ninguna tabla innecesaria. Después seguirá SQL-07: carga de prueba con una muestra pequeña.