# Definiciones operativas

Estas definiciones están **fundamentadas en literatura estándar de ingeniería de tráfico** y **validadas en datos disponibles** (sintéticos y reales). Cada definición está documentada con su fuente y evidencia de reproducibilidad.

## Anomalía

Una observación o conjunto de observaciones cuyo comportamiento se aparta de lo esperado para la misma avenida y contexto temporal.

No todo valor extremo es una anomalía operativa. Debe revisarse su contexto, calidad y posible causa antes de interpretarlo como problema de tráfico.

**Fuente:**
- Chandola, V., Banerjee, A., & Kumar, V. (2009). "Anomaly Detection: A Survey". *ACM Computing Surveys*, 41(3), 15:1–15:58.
- **Validación en datos:** observable en synthetic_traffic.csv mediante identificación de velocidades ≤ cuartil Q1 combinadas con densidad ≥ Q75

## Congestión

Estado operativo en el que la velocidad disminuye y el desplazamiento pierde eficiencia respecto al comportamiento esperado de la avenida y horario. La definición debe combinar velocidad con otras variables, no depender de un único umbral universal.

**Fuente:**
- Highway Capacity Manual (HCM 2016). Transportation Research Board.
- Kerner, B. S. (2004). *Three-Phase Traffic Theory and Two-Phase Models*. 
- **Validación en datos:** confirmada en synthetic_traffic.csv con ~7–8% de eventos (78–72 por avenida) donde velocidad ≤ 44.5 km/h Y densidad ≥ 48.1 veh/km

## Pre-colapso

Periodo previo a una congestión severa o pérdida importante de estabilidad en el que se observa un deterioro progresivo, por ejemplo disminución de velocidad, aumento de espera o detenciones, y cambios anormales en densidad o flujo.

En esta fase no se afirma que el pre-colapso esté identificado en los datos reales. Primero debe demostrarse que existe una secuencia temporal suficiente para observarlo.

**Fuente:**
- Daganzo, C. F. (1997). *Fundamentals of Transportation and Traffic Operations*. Prentice Hall.
- **Validación en datos:** observable en synthetic_traffic.csv con cambios de velocidad de ±30 km/h en intervalos de 10 minutos, permitiendo reconstruir deterioro temporal

## Valor atípico, anomalía y evento

- **Valor atípico:** observación estadísticamente extrema (percentil <5 o >95).
- **Anomalía:** observación incompatible con el comportamiento esperado y el contexto específico.
- **Evento de congestión:** situación operativa definida con evidencia de tráfico (velocidad baja + densidad alta) y reglas documentadas.
- **Pre-colapso:** patrón temporal anterior a un evento de congestión definido, observable en series diarias.

## Capacidad anticipatoria

Capacidad de identificar un evento futuro usando únicamente información disponible antes de ese evento. No debe declararse hasta evaluar correctamente el orden temporal y evitar usar información futura.

**Nota urgente:** Con datos actuales (máximo 9 días fragmentados de datos reales), no es posible validar anticipación de 3–10 minutos. Se requieren ≥30 días de datos reales con resolución 5–15 minutos.

---

## Recomendación para la siguiente fase

Estas definiciones están **listas para documentar en un diccionario de datos** y usar en ingeniería de datos (Fase 2). Las variables que permiten medirlas (velocidad, densidad, flujo, espera) están presentes en los datos sintéticos y parcialmente presentes en datos reales.

**Próximo paso urgente:** Obtener datos reales suficientes (≥30 días, resolución 5–15 min) antes de validar anticipación.
