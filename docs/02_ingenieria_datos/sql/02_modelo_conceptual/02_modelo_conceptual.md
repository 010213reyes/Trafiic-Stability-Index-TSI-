# SQL-02: modelo conceptual internacional

## Objetivo

Definir las entidades de la base internacional sin fijar todavía tipos SQL ni detalles de implementación.

## Entidades

- **Ciudad:** contexto geográfico y zona horaria de cada fuente.
- **Fuente:** procedencia, rol, licencia y características documentadas del dataset.
- **Segmento:** sensor, tramo, agregado o identificador equivalente de la fuente.
- **Observación de tráfico:** medición temporal asociada con ciudad, fuente y segmento.
- **Calidad de observación:** advertencias o problemas vinculados a una observación.
- **Agregado analítico:** resumen temporal preparado para consultas posteriores.
- **Carga:** trazabilidad de cada lote leído, insertado o rechazado.

## Relaciones

```text
Ciudad 1 ─── N Fuente
Ciudad 1 ─── N Segmento
Fuente 1 ─── N Segmento
Ciudad 1 ─── N Observacion
Fuente 1 ─── N Observacion
Segmento 1 ─ N Observacion
Observacion 1 ─ N CalidadObservacion
Ciudad/Fuente/Segmento 1 ─ N AgregadoAnalitico
Fuente 1 ─── N Carga
```

## Límites

- No se crean tablas por ciudad ni por métrica.
- Los resultados de Isolation Forest, LOF y DBSCAN quedan fuera de las observaciones originales.
- Las diferencias entre velocidad, intensidad, índice y longitud de congestión se conservan mediante la política de métricas de SQL-04.
- Las tablas de usuarios y sesiones pertenecen a la aplicación, no a esta base analítica.