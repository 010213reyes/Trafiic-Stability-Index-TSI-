# SQL-04: política de representación de métricas

## Decisión

Se utilizará un modelo híbrido:

1. Las métricas conocidas se conservarán como columnas en `fact_observaciones`.
2. `metrica_principal` identificará la métrica central del registro.
3. `valor_principal` conservará el valor de esa métrica.
4. Las variables que una fuente no mida permanecerán nulas.
5. Los valores originales dudosos se conservarán en columnas con sufijo `_fuente`.

Esta decisión mantiene la facilidad de análisis del modelo de columnas sin obligar a que todas las ciudades midan lo mismo.

## Mapeo por fuente

| Fuente | `metrica_principal` | `valor_principal` | Columnas complementarias | Comparación directa |
|---|---|---|---|---|
| Istanbul | `indice_congestion` | promedio del índice | mínimo y máximo del índice | Solo con otros índices compatibles |
| São Paulo | `congestion_longitud_m` | `jam_size` | dirección, región y tipo de vía | Solo con longitud de congestión |
| Madrid | `intensidad` | `intensidad_fuente` | ocupación, carga y `vmed_fuente` | Intensidad con intensidad documentada |
| METR-LA | `velocidad_sensor` | `valor_fuente` | sensor y tipo de vía | Velocidad con velocidad compatible |
| PEMS-BAY | `velocidad_sensor` | `valor_fuente` | sensor y tipo de vía | Velocidad con velocidad compatible |

## Reglas de equivalencia

### Comparables directamente, si comparten unidad y significado

- METR-LA y PEMS-BAY: velocidad de sensor contra velocidad de sensor.
- Madrid e intensidad de otra fuente: solo después de confirmar unidad y método.
- Índices de congestión: solo si documentan la misma escala y definición.

### No comparables directamente

- velocidad contra longitud de congestionamiento;
- intensidad contra ocupación;
- ocupación contra densidad;
- índice agregado contra medición de sensor;
- carga de Madrid contra flujo vehicular sin documentación adicional.

## Reglas para Madrid

- `intensidad_fuente` conserva el valor original de intensidad.
- `flujo_veh_h` no se considerará confirmado hasta documentar que la unidad representa vehículos por hora.
- `vmed_fuente` no se renombrará definitivamente como `velocidad_kmh` hasta confirmar su unidad.
- `ocupacion_pct` se conserva como ocupación y no se transforma en densidad.

## Reglas para Istanbul

- Se representa como una observación agregada.
- `segmento_id` utiliza `istanbul_aggregate_index`.
- No se crean sensores ficticios.
- No se convierte el índice a velocidad, densidad o flujo.

## Reglas para São Paulo

- `jam_size` se conserva como `congestion_longitud_m`.
- No se convierte longitud de congestión en velocidad.
- `segmento_id` representa el segmento original del conjunto.
- Los duplicados eliminados permanecen documentados en el reporte de calidad.

## Reglas para METR-LA y PEMS-BAY

- `valor_fuente` se conserva hasta confirmar la unidad en la documentación del dataset.
- La fuente se identifica como red de autopistas.
- No se presentan como observaciones de Guadalajara.
- No se inventan flujo, ocupación ni densidad.

## Qué no se crea

No se crea una tabla de métricas con una fila por cada valor para esta primera versión. Esa estructura multiplicaría el volumen y complicaría el cálculo del TSI sin aportar una necesidad actual.

Si en el futuro aparecen muchas métricas nuevas o fuentes con esquemas muy variables, se podrá revisar esta decisión con evidencia.

## Resultado de SQL-04

La tabla principal conservará varias columnas métricas y una pareja explícita de identificación:

```text
metrica_principal
valor_principal
```

La comparación se hará por familias de métricas y no por una mezcla indiscriminada de todas las fuentes.

## Criterio de aprobación

SQL-04 queda aprobado cuando esta política sea aceptada. El siguiente paso será SQL-05: asignar tipos, restricciones e índices para MySQL sin modificar el significado de las métricas.