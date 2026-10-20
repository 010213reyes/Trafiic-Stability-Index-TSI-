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

La validacion queda preparada, pero no se considera cerrada hasta que la carga completa de MySQL termine y el archivo `estado.json` indique `completa`.

No se debe repetir la carga de prueba de 5.000 filas como sustituto de la validacion final.
