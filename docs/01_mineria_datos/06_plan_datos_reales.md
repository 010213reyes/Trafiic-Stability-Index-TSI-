# Plan de obtención de datos reales de tráfico

## Situación actual

- **Datos sintéticos:** 5,040 observaciones, 6–7 días, resolución 10 min ✓ apto para prototipo
- **Datos reales:** 427 observaciones, máximo 9 días, resolución inconsistente ✗ insuficiente

**Problema:** Un modelo entrenado solo en datos sintéticos no funcionará en producción.

## Requisitos de datos reales

Para validar la hipótesis de anticipación de 3–10 minutos y crear un modelo operativo:

| Aspecto | Requisito | Actual | Estado |
|---------|-----------|--------|--------|
| Cobertura temporal | ≥30 días | máx. 9 días | ✗ Falta 21 días |
| Resolución | 5–15 minutos | inconsistente | ✗ No garantizado |
| Avenidas | ≥3 avenidas principales | 6–9 por fuente | ✓ Parcial |
| Variables | velocidad, densidad, flujo, espera, detenciones | presentes pero inconsistentes | ✓ Parcial |
| Continuidad | serie sin huecos significativos | fragmentada | ✗ Huecos documentados |

## Opciones de recolección

### Opción 1: Autoridades de tránsito municipal/estatal
**Fuente:** Secretaría de Movilidad, Instituto de Transporte y Vialidad, o equivalente local

**Cómo acceder:**
1. Solicitar datos abiertos o acceso API a los sistemas de monitoreo existentes
2. Especificar: avenidas principales (Chapultepec, México, Universidad, etc.), período (30 días), resolución (5–15 min)
3. Formatos típicos: CSV, JSON, consulta API

**Ventajas:** Datos reales, alta confiabilidad, variables estándar
**Desventajas:** Tramites administrativos, tiempo de respuesta, posibles restricciones de licencia
**Probabilidad:** Moderada (depende de políticas de datos abiertos locales)

### Opción 2: Plataformas de movilidad urbana
**Fuente:** Waze, Google Maps, Mapbox (APIs de tráfico)

**Cómo acceder:**
1. Registrarse en consola de desarrollador
2. Consultar tráfico histórico (si está disponible) o recolectar en tiempo real durante 30 días
3. Variables: velocidad, congestión, tiempos de recorrido

**Ventajas:** Datos reales, acceso sin tramites, cobertura de múltiples avenidas
**Desventajas:** Costos por llamadas a API, limitaciones de resolución histórica, precisión variable
**Probabilidad:** Alta (acceso inmediato, pero con costo)

**Ejemplo de costo estimado:**
- Google Maps Traffic API: ~$7–15 USD por 1,000 consultas
- 30 días × 144 consultas/día (cada 10 min) × 5 avenidas ≈ 21,600 consultas ≈ $150–300 USD
- Waze Premium data (si disponible): comúnmente $100–500 USD/mes

### Opción 3: Sensores IoT / cámaras de tráfico
**Fuente:** Sistemas de conteo de vehículos en campo

**Cómo acceder:**
1. Instalar sensores en intersecciones clave (costly)
2. Conectar a plataforma de recolección
3. Exportar datos después de 30 días de monitoreo

**Ventajas:** Datos de máxima precisión, control total
**Desventajas:** Muy costoso (€1,000–5,000 USD por sensor), tiempo de instalación
**Probabilidad:** Baja (impractible para proyecto académico)

### Opción 4: Datos históricos + simulación mejorada
**Fuente:** Extender datos actuales + mejorar modelo sintético

**Cómo acceder:**
1. Usar las 427 observaciones reales existentes para calibrar un modelo de simulación (SUMO, MATSim)
2. Generar 30 días simulados usando patrones de tráfico real observados
3. Usar sintéticos calibrados como aproximación

**Ventajas:** Bajo costo, control total, combina lo mejor de ambos mundos
**Desventajas:** Requiere experto en simulación, resultado sigue siendo "cuasi-sintético"
**Probabilidad:** Moderada

## Recomendación

**Prioridad 1 (Inmediato):**
1. Contactar Secretaría de Movilidad local → solicitar datos abiertos o acceso API
2. Paralelamente, evaluar costo de Google Maps Traffic API
3. Plazo: 1–2 semanas

**Prioridad 2 (Si Prioridad 1 falla):**
1. Implementar recolección automática vía Google Maps API por 30 días
2. Presupuesto: ~$200 USD
3. Plazo: 40 días (30 recolección + 10 análisis)

**Prioridad 3 (Fallback):**
1. Usar datos sintéticos calibrados para prototipo académico
2. Documentar limitaciones explícitamente
3. Advertir que modelo no es operativo sin datos reales

## Próximos pasos

Después de cerrar minería (documentar fuentes de definiciones):

1. **Semana 1:** Iniciar gestión de datos reales (Prioridad 1)
2. **Semana 2–4:** Ingeniería de datos (Fase 2) en paralelo
3. **Semana 4+:** Con datos reales en hand → pasar a análisis y modelado

**No iniciar análisis ni ML hasta tener datos reales confirmados.**
