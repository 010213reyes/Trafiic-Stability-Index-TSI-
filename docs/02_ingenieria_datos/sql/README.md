# Fase SQL internacional

La fase SQL está organizada por subfases para separar decisiones, modelos, cargas y validaciones. La entrada oficial es `data/02_clean/consolidated/international_observations.parquet`.

| Carpeta | Fase | Estado |
|---|---|---|
| `00_planificacion` | Plan general de SQL | Actualizado hasta SQL-09 |
| `01_alcance` | Preguntas y límites | Completada |
| `02_modelo_conceptual` | Entidades y relaciones conceptuales | Completada |
| `03_modelo_logico` | Tablas, claves y cardinalidades | Completada |
| `04_politica_metricas` | Separación semántica de métricas | Completada |
| `05_modelo_fisico` | Tipos, restricciones e índices MySQL | Completada |
| `06_diagrama_eer` | Modelo visual de Workbench | Completada |
| `07_carga_prueba` | Prueba internacional de 5.000 filas | Completada |
| `08_carga_controlada` | Plan y DDL para carga por lotes | Planificada, no ejecutada |
| `09_validacion` | Consultas de control | Preparadas, pendientes de MySQL |
| `legacy_prototipo` | SQLite de la investigación anterior | Fuera de la base internacional |

No se deben mezclar los artefactos de `legacy_prototipo` con SQL-07, SQL-08 o SQL-09.