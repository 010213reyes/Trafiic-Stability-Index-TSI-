# Pipeline SQL TSI

Esta carpeta contiene el esquema MySQL de la investigación internacional TSI. Los scripts están separados por tabla, pero deben ejecutarse respetando el orden del archivo maestro.

## Orden de ejecución

Desde la raíz del repositorio:

```powershell
mysql -u TU_USUARIO -p < docs/02_ingenieria_datos/sql/pipelines_sql/00_crear_base.sql
```

El archivo maestro crea `tsi_db`, selecciona `utf8mb4` y ejecuta las tablas en este orden:

1. `dim_ciudad`
2. `dim_fuente`
3. `dim_segmento`
4. `fact_observaciones`
5. `calidad_observacion`
6. `fact_agregado`
7. `log_cargas`
8. índices de observaciones

El comando `SOURCE` del maestro debe ejecutarse con el directorio actual situado en la raíz del repositorio. En MySQL Workbench también se pueden abrir los archivos individualmente en el mismo orden.

## Conexión desde VS Code

Instala una extensión de conexión MySQL, por ejemplo SQLTools y su driver MySQL/MariaDB. Crea una conexión local con los datos de tu instalación de MySQL, selecciona la base `tsi_db` y ejecuta primero `00_crear_base.sql`.

No guardes contraseñas en este repositorio. Usa el administrador de credenciales de la extensión o variables de entorno locales.

## Comprobación

Después de crear el esquema, ejecuta `seleccion_tsi.sql`. Debe devolver la base seleccionada y una consulta agrupada por ciudad, fuente y métrica principal.

Esta carpeta solo crea la estructura. La carga del consolidado internacional de 41.770.880 observaciones se realizará después, mediante el cargador controlado de SQL-08.