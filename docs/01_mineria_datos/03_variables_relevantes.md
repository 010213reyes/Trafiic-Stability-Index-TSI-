# Variables relevantes para el TSI

## Variables candidatas

| Variable conceptual | Nombres observados | Posible función |
|---|---|---|
| Tiempo | `timestamp`, `hour` | Orden temporal, ventanas y comparación por horario |
| Avenida | `avenida`, `road` | Comparar comportamiento por vía |
| Velocidad | `velocidad`, `velocity_kmh`, `speed_kmh`, `avg_speed` | Señal principal de pérdida de eficiencia |
| Densidad | `densidad`, `density_veh_km` | Contexto de carga vehicular |
| Flujo | `flow_veh_h` | Relación entre movimiento y carga; solo existe directamente en la fuente sintética |
| Espera | `wait_time_sec` | Severidad operativa; disponible directamente en la fuente sintética |
| Detenciones | `detenciones`, `stops_count` | Irregularidad y pérdida de fluidez |
| Confianza | `confidence`, `avg_confidence` | Fiabilidad de reportes crowdsourcing |
| Reportes | `report_type`, `congestion_reports` | Evidencia aportada por usuarios |
| Usuarios | `user_id`, `unique_users` | Cobertura y posible concentración de participación |
| Ubicación | `latitud`, `longitud`, `latitude`, `longitude` | Validación espacial y agrupación geográfica |

## Variables prioritarias

1. Timestamp normalizado.
2. Avenida normalizada.
3. Velocidad.
4. Densidad, si se confirma su unidad y calidad.
5. Detenciones.
6. Confianza y número de usuarios para crowdsourcing.
7. Flujo y espera como variables complementarias, no como variables disponibles de forma uniforme.

## Criterios de selección

Una variable será candidata final si:

- Tiene significado operativo claro.
- Tiene unidad conocida.
- Está disponible en una proporción suficiente de registros.
- Puede compararse entre avenidas y fuentes.
- No introduce información del futuro.
- Puede calcularse de forma reproducible.

## Advertencia

No se debe construir todavía una tabla unificada ni combinar columnas con nombres parecidos hasta resolver unidades, escalas, nombres de avenida y reglas de agregación.
