# SQL-07: resultado de la carga de prueba internacional

## Objetivo

Validar el modelo relacional internacional con una muestra reproducible del consolidado, sin modificar la SQLite del prototipo anterior ni cargar los 41.770.880 registros.

## Ejecución

```powershell
.\.venv\Scripts\python.exe docs\02_ingenieria_datos\sql\07_carga_prueba_internacional.py --rows-per-source 1000
```

La entrada fue `data/02_clean/consolidated/international_observations.parquet`. La muestra selecciona las primeras 1.000 observaciones disponibles por fuente:

| Fuente | Filas |
|---|---:|
| `istanbul_traffic_index` | 1.000 |
| `sao_paulo_cet` | 1.000 |
| `madrid_traffic_points` | 1.000 |
| `metr_la` | 1.000 |
| `pems_bay` | 1.000 |
| **Total** | **5.000** |

## Resultado

La carga fue exitosa y se generaron:

- `dim_ciudad`: 5 filas;
- `dim_fuente`: 5 filas;
- `dim_segmento`: 232 filas;
- `fact_observaciones`: 5.000 filas;
- `log_cargas`: 5 filas;
- `calidad_observacion` y `fact_agregado`: creadas vacías para esta prueba.

Validaciones ejecutadas:

- violaciones de claves foráneas: 0;
- nulos en campos obligatorios de hechos: 0;
- identificadores de observación duplicados: 0;
- estado general: `passed`.

## Decisión sobre `tipo_via`

El consolidado contiene algunos `tipo_via` nulos, mientras que el modelo físico exige ese campo en `dim_segmento`. Para no eliminar observaciones, la carga de staging transforma únicamente ese valor ausente en `no_especificado`. Las métricas ausentes permanecen como `NULL` y no se imputan.

## Artefactos

- Script reproducible: `07_carga_prueba_internacional.py`.
- Base de prueba: `tsi_international_stage.sqlite`.
- Manifiesto: `sql07_international_load_manifest.json`.

La base de prueba no es todavía la base definitiva de producción. El siguiente paso es SQL-08: decidir y probar la carga controlada del consolidado completo por lotes.