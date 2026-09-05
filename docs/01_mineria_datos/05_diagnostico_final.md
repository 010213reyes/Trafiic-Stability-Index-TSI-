# Diagnóstico de la Fase 1: Minería de datos

## Estado

La minería de datos está **iniciada y parcialmente documentada**. Ya existe evidencia suficiente para delimitar el problema y los riesgos, pero la fase todavía no está cerrada.

## Diagnóstico actual

El proyecto cuenta con cinco archivos raw provenientes de fuentes sintéticas, históricas/base, scraping y crowdsourcing. Las fuentes tienen esquemas, periodos, unidades y niveles de calidad diferentes. Por ello, todavía no deben combinarse directamente.

La velocidad, el tiempo y la avenida son las variables con mayor presencia transversal. Densidad, detenciones, confianza, reportes y usuarios aportan contexto, pero su disponibilidad cambia según la fuente. Flujo y tiempo de espera no están disponibles de manera uniforme.

### Análisis de reproducibilidad (evidencia 2026-09-05)

Se ejecutó un análisis controlado para determinar si las definiciones de congestión y pre-colapso son **reproducibles y observables** en los datos existentes:

**✓ SYNTHETIC_TRAFFIC.CSV - APTO para validación de definiciones**
- Registros: 5,040
- Resolución: 10 minutos
- Cobertura: 6–7 días
- Avenidas: 5 únicas
- Variables críticas: velocidad (20–80 km/h), densidad (5–99 veh/km), flujo, espera, detenciones
- Patrones observados:
  - **Congestión (baja velocidad + alta densidad):** detectada en ~7–8% de observaciones (78–72 eventos por avenida)
  - Velocidad media: 52–53 km/h, con eventos de congestión a ~38 km/h
  - **Deterioro temporal:** cambios de ±30 km/h en intervalos de 10 minutos, permitiendo observar pre-colapso

**✗ TRAFFIC_DATA.CSV + SCRAPED_TRAFFIC.CSV - INSUFICIENTES para validación**
- Observaciones totales: 310 + 117 = 427 (vs. 5,040 sintéticos)
- Resolución temporal: inconsistente, sin garantía de 10 minutos
- Cobertura máxima: 9 días fragmentados
- Faltantes: 0% en velocidad/densidad, pero escasez extrema de densidad por avenida
- **Impacto:** no permiten observar pre-colapso ni validar anticipación de 3–10 minutos

**Conclusión:** Los datos sintéticos son **reproducibles y suficientes para validar las definiciones de congestión**. Los datos reales actuales son demasiado escasos.

## Definición de trabajo

- **Anomalía:** comportamiento que se aparta de lo esperado para una avenida y contexto temporal. *Fuente: Chandola et al. (2009) "Anomaly Detection: A Survey"; validado en datos sintéticos.*
- **Congestión:** pérdida de eficiencia operativa respecto al comportamiento esperado, evaluada con múltiples variables (velocidad baja + densidad alta, no un umbral universal). *Fuente: Highway Capacity Manual (HCM 2016), Transportation Research Board; observable en synthetic_traffic.csv.*
- **Pre-colapso:** deterioro temporal anterior a un evento de congestión severa, con cambios progresivos en velocidad, espera o densidad. *Fuente: Daganzo (1997) "Fundamentals of Transportation and Traffic Operations"; observable en datos sintéticos cada 10 minutos.*

**Validación en datos:**
- Congestión: confirmada en synthetic_traffic.csv (7–8% de eventos)
- Pre-colapso: patrones de deterioro de ±30 km/h en intervalos de 10 minutos, observable en series diarias
- Fuentes reales: aún insuficientes para validar (solo 427 observaciones)

Estas definiciones están **alineadas con literatura estándar de ingeniería de tráfico** y **reproducibles en los datos sintéticos disponibles**. Están listos para documentar en diccionario de datos.

## Respuesta a la hipótesis de 3 a 10 minutos

**DECISIÓN EXPLÍCITA:** No se puede validar anticipación de 3–10 minutos con los datos actuales.

**Razones:**

1. **Datos sintéticos:** tienen resolución adecuada (10 minutos) pero no constituyen evidencia real de comportamiento de tráfico urbano.
2. **Datos reales:** muy escasos (427 observaciones vs. 5,040 sintéticas); máximo 9 días de cobertura fragmentada.
3. **Requisitos faltantes:**
   - Mínimo 30 días de datos reales (actual: máximo 9 días)
   - Variables consistentes en todas las avenidas (actual: inconsistentes en traffic_data.csv y scraped_traffic.csv)
   - Resolución garantizada de 5–15 minutos (actual: en dudas)

**Plan de validación (futuro):**
1. Obtener ≥30 días de datos reales con resolución 5–15 minutos
2. Definir evento de congestión objetivo con etiquetas verdaderas
3. Construir variables usando solo información previa (sin data leakage)
4. Medir anticipación, falsos positivos y falsos negativos
5. Evaluar si 3–10 minutos es realista o debe ajustarse

**Nota urgente:** Sin datos reales suficientes, cualquier modelo entrenado en datos sintéticos no será válido en producción.

## Decisiones para la siguiente fase

1. **No crear otro scraper todavía.** Primero evaluar si los datos reales actuales pueden complementarse (expansión) o si la estrategia de recolección es fundamentalmente diferente (nuevas fuentes).
2. **No unir fuentes hasta tener diccionario de datos** que normalice nombres de avenida, unidades, resolución temporal.
3. **Prioritario:** Obtener datos reales de tráfico urbano con resolución 5–15 minutos, mínimo 30 días, múltiples avenidas.
4. Corregir rutas antiguas `data/raw/` y `data/processed/` durante ingeniería de datos (fase 2).
5. Mantener `00_raw` sin modificaciones; todas las transformaciones en `01_processed/` y posteriores.

## Criterio para cerrar minería

La Fase 1 se considera **CERRADA cuando estén aprobados:**

- ✓ Definiciones operativas documentadas con fuentes (literatura + validación en datos)
- ✓ Catálogo de fuentes con estadísticas de cobertura y calidad
- ✓ Variables identificadas, con unidades y rangos
- ✓ Riesgos y sesgos documentados
- **[PENDIENTE]** Plan explícito para obtener datos reales (≥30 días, resolución 5–15 min)
- **[PENDIENTE]** Diccionario de datos preliminar (nombres, tipos, unidades)

## Recomendación para decisor

**Los datos sintéticos son suficientes para prototipar definiciones y modelos**, pero **no son suficientes para validar anticipación**. 

Para que el proyecto sea válido en producción, se **requiere obtener datos reales de tráfico urbano** antes de pasar a ingeniería de datos (fase 2) o modelado (fase 4).

Sin este paso, cualquier modelo será un prototipo académico, no una herramienta operativa.
