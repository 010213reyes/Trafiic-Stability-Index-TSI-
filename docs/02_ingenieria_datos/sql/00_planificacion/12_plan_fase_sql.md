# Plan de la fase SQL

## Objetivo

Construir una base de datos relacional para consultar las observaciones limpias y consolidadas del proyecto TSI, conservando la trazabilidad de ciudad, fuente, segmento, métrica y calidad del registro.

La base SQLite existente (`docs/02_ingenieria_datos/sql/legacy_prototipo/tsi_stage.sqlite`) se considera un prototipo previo. Su manifiesto indica que fue cargada con el dataset clean anterior y un límite de 50,000 filas; no representa todavía la base SQL final de las fuentes internacionales.

## Entrada oficial de esta fase

La entrada será:

`data/02_clean/consolidated/international_observations.parquet`

No se cargarán directamente archivos raw, ZIP, notebooks, imágenes ni resultados de algoritmos como si fueran observaciones originales.

## Subfases

### SQL-01. Alcance y preguntas de consulta

Definir qué preguntas debe responder la base:

- observaciones por ciudad, fuente, segmento y periodo;
- métricas disponibles por fuente;
- calidad, nulos y advertencias;
- comparación de volumen y cobertura entre ciudades;
- resultados agregados para el análisis posterior.

**Salida:** lista de preguntas y límites del modelo.

### SQL-02. Modelo conceptual

Dibujar las entidades sin tipos SQL todavía:

- ciudad;
- fuente;
- segmento;
- observación de tráfico;
- registro de calidad;
- agregado analítico.

**Salida:** diagrama conceptual revisado.

### SQL-03. Modelo lógico

Convertir las entidades en tablas, definir claves primarias, claves foráneas, cardinalidades y campos obligatorios.

**Salida:** esquema lógico y diccionario preliminar.

### SQL-04. Separación de métricas

Decidir qué métricas permanecen como columnas y cómo se conserva `metrica_principal` y `valor_principal` sin mezclar velocidad, intensidad, índice y longitud de congestión.

**Salida:** regla documentada de representación de métricas.

### SQL-05. Modelo físico para MySQL

Asignar tipos MySQL, tamaños, restricciones, índices y nombres definitivos.

**Salida:** diseño físico listo para Workbench.

### SQL-06. Diagrama EER en MySQL Workbench

Construir visualmente el modelo, revisar relaciones y corregir redundancias antes de crear la base.

**Salida:** modelo visual y guía de construcción.

### SQL-07. Carga de prueba

Cargar primero una muestra pequeña y representativa del consolidado para comprobar tipos, claves, nulos y tiempos de carga.

**Salida:** base de prueba y reporte de errores.

### SQL-08. Carga controlada del consolidado

Definir si la carga completa será local, por lotes o mediante archivos intermedios. La decisión debe considerar que el consolidado tiene aproximadamente 41.7 millones de filas.

**Salida:** carga reproducible y manifiesto de ejecución.

### SQL-09. Consultas de validación

Verificar conteos, fuentes, ciudades, rangos, fechas, nulos y relaciones entre tablas.

**Salida:** consultas de control y resultados documentados.

### SQL-10. Base lista para análisis

Entregar la base validada para EDA y modelado, sin convertir resultados de algoritmos en datos originales.

**Salida:** base SQL documentada y lista para análisis.

## Orden de trabajo

```text
SQL-01 preguntas
    ↓
SQL-02 modelo conceptual
    ↓
SQL-03 modelo lógico
    ↓
SQL-04 métricas
    ↓
SQL-05 modelo físico MySQL
    ↓
SQL-06 diagrama Workbench
    ↓
SQL-07 carga de prueba
    ↓
SQL-08 carga controlada
    ↓
SQL-09 validaciones
    ↓
SQL-10 base lista para análisis
```

## Regla de control

No se crearán tablas definitivas ni scripts de carga hasta aprobar el modelo conceptual y lógico. Primero se dibuja, se revisa y se elimina cualquier tabla que no responda una pregunta concreta del proyecto.

## Estado inicial

- SQL-01: completado; preguntas y límites documentados en `../01_alcance/01_alcance_preguntas.md`.
- SQL-02: completado; carpeta reservada en `../02_modelo_conceptual/`; el artefacto conceptual debe conservarse allí.
- SQL-03: completado; modelo lógico en `../03_modelo_logico/03_modelo_logico.md`, pendiente de revisión en papel.
- SQL-04: completado; política de métricas en `../04_politica_metricas/04_politica_metricas.md`.
- SQL-05: completado; modelo físico en `../05_modelo_fisico/05_modelo_fisico_mysql.md`.
- SQL-06: completado; diagrama y guía en `../06_diagrama_eer/06_diagrama_eer_workbench.md`.
- SQL-07: completado; carga internacional de 5.000 filas validada en `../07_carga_prueba/07_resultado_carga_prueba_internacional.md`.
- SQL-08: planificado; carga por lotes hacia MySQL documentada en `../08_carga_controlada/08_plan_carga_controlada.md`.
- SQL-09: consultas preparadas en `../09_validacion/09_consultas_validacion_mysql.sql`; ejecución pendiente de la instancia MySQL.
- Prototipo SQLite anterior: existente, pero separado de la nueva base internacional.
- Consolidado internacional: disponible como entrada.
- Guía visual de MySQL Workbench: se elaborará después de aprobar SQL-03 y antes de SQL-07.