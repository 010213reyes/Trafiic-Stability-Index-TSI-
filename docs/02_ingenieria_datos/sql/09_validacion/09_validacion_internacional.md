# SQL-09: validación de la base internacional

## Alcance

Las consultas de `09_consultas_validacion_mysql.sql` validan la base creada en SQL-08 en cinco dimensiones:

- conteos generales y cobertura por fuente;
- fechas y métricas principales;
- nulos en campos obligatorios;
- relaciones huérfanas entre hechos y dimensiones;
- rangos imposibles y trazabilidad de lotes.

## Criterios de aprobación

La base podrá avanzar a SQL-10 cuando:

- el conteo de `fact_observaciones` coincida con el manifiesto de carga;
- cada fuente conserve su métrica principal sin mezcla semántica;
- no existan nulos en las claves obligatorias;
- no existan relaciones huérfanas;
- no existan ocupaciones fuera de 0 a 100 ni valores físicos negativos;
- `filas_insertadas + filas_rechazadas` sea igual a `filas_leidas` por lote.

## Estado

Las consultas están preparadas, pero quedan pendientes de ejecución hasta disponer de la instancia MySQL de SQL-08. La prueba SQLite de SQL-07 ya validó el mismo conjunto básico de claves y campos obligatorios.