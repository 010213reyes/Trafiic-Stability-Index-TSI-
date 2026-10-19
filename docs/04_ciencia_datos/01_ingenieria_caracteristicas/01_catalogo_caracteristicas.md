# Catalogo inicial de caracteristicas

Este catalogo define variables candidatas antes de entrenar modelos. Ninguna variable se considera aprobada hasta verificar unidad, frecuencia y disponibilidad por fuente.

## Caracteristicas temporales

| Caracteristica | Regla | Disponibilidad |
|---|---|---|
| `hora` | Hora derivada de `timestamp` | Todas las fuentes |
| `dia_semana` | Dia de semana derivado de `timestamp` | Todas las fuentes |
| `mes` | Mes derivado de `timestamp` | Todas las fuentes |
| `periodo_pico` | Regla documentada sobre hora local | Solo tras confirmar zona horaria |

## Caracteristicas de nivel

| Caracteristica | Regla | Restriccion |
|---|---|---|
| `nivel_metrica` | `valor_principal` sin cambiar su semantica | No comparar entre metricas distintas |
| `nivel_normalizado_fuente` | Normalizacion dentro de ciudad y fuente | No usar como comparacion internacional final |
| `calidad_registro` | Etiqueta original de calidad | Usar como filtro o variable de control |

## Caracteristicas de cambio

| Caracteristica | Regla | Restriccion |
|---|---|---|
| `delta_metrica` | Diferencia contra observacion anterior | Requiere frecuencia regular por fuente y segmento |
| `tasa_cambio_metrica` | Diferencia dividida entre minutos transcurridos | No calcular con intervalos desconocidos |
| `variabilidad_ventana` | Desviacion en ventana temporal | Requiere ventana con observaciones suficientes |
| `tendencia_ventana` | Pendiente de la metrica en ventana | No mezclar ventanas de distinta duracion |

## Caracteristicas de anticipacion

| Caracteristica | Regla | Condicion |
|---|---|---|
| `valor_futuro_18_20_min` | Valor posterior en la ventana objetivo | Solo donde exista frecuencia compatible |
| `cambio_futuro` | Diferencia entre valor actual y futuro | No usar como predictor si genera fuga temporal |
| `etiqueta_pre_colapso` | Regla operacional de deterioro futuro | Pendiente de definir y validar con Guadalajara |

## Variables excluidas inicialmente

- Mezclas directas entre `indice_congestion`, `intensidad`, `congestion_longitud_m` y `velocidad_sensor`.
- Promedios internacionales sin normalizacion y alineacion temporal.
- Variables futuras usadas como entrada del mismo instante.
- Imputaciones no documentadas para campos que una fuente no mide.

## Criterio de aprobacion

Una caracteristica se incorpora al modelado solo si tiene fuente, unidad, ventana, regla de calculo, cobertura esperada y prueba contra fuga temporal documentadas.
