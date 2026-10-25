# 06 Validacion SQL

Esta subfase valida que MySQL conserve el mismo universo analitico que el consolidado Parquet despues de la carga completa.

## Ejecucion

Configura las variables locales sin escribir credenciales en el repositorio:

```powershell
$env:TSI_MYSQL_HOST = "127.0.0.1"
$env:TSI_MYSQL_PORT = "3306"
$env:TSI_MYSQL_USER = "root"
$env:TSI_MYSQL_DATABASE = "tsi_db"
.\.venv\Scripts\python.exe docs\03_analisis_datos\06_validacion_sql\06_validacion_sql.py --password
```

El script compara:

- conteo total de `fact_observaciones`;
- conteo por ciudad, fuente y metrica principal;
- fecha minima y maxima por grupo;
- grupos ausentes o adicionales;
- diferencias de observaciones.

Las salidas locales se guardan en `data/03_analysis_output/validacion_sql/`.

## Estado actual

La carga completa de MySQL ya termino y contiene `41,770,880` observaciones. Los conteos por fuente coinciden con el consolidado Parquet:

- `istanbul_traffic_index`: `3,332`;
- `madrid_traffic_points`: `12,512,133`;
- `metr_la`: `7,094,304`;
- `pems_bay`: `16,937,700`;
- `sao_paulo_cet`: `5,223,411`.

La validacion queda cerrada mediante `data/03_analysis_output/validacion_sql/estado.json`, con estado `completa`, diferencia total `0` y metodo `validacion_manual_sql_por_fuente`.

El script automatico conserva una consulta adicional de rangos y grupos, pero no es necesario repetir la carga ni ejecutar el cargador para validar la base. La carga de prueba de 5.000 filas tampoco sustituye la carga internacional completa.
