# Plan de inicio del analisis

## Alcance

Analizar el consolidado internacional limpio antes de completar la carga total en MySQL. El objetivo es conocer la estructura, cobertura, calidad y comportamiento de las fuentes que alimentaran el TSI.

## Preguntas iniciales

1. Que ciudades y fuentes tienen cobertura suficiente para el analisis?
2. Cual es la frecuencia temporal real de cada fuente?
3. Que porcentaje de valores nulos, duplicados y registros fuera de rango existe?
4. Como se distribuye la metrica principal de cada fuente?
5. Que transformaciones son necesarias para comparar fuentes sin mezclar significados?
6. Que limitaciones deben conservarse al calibrar y validar Guadalajara?

## Primer entregable

El primer entregable sera un EDA reproducible con:

- conteo de observaciones por ciudad y fuente;
- cobertura minima y maxima de fechas;
- completitud por campo;
- estadisticos de la metrica principal por fuente;
- frecuencia temporal y granularidad;
- registro de incidencias y decisiones analiticas.

## Fuente y dependencia SQL

La ejecucion inicial usara `data/02_clean/consolidated/international_observations.parquet`. La validacion equivalente en MySQL se ejecutara despues de completar la carga controlada y se documentara en `06_validacion_sql`.

## Criterio de avance

No se construira un indicador comparativo final hasta documentar la semantica, unidad, rango y cobertura de cada metrica.
