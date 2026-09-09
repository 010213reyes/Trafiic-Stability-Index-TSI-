# Plan de obtención de datos reales de tráfico

## Situación actual

- **Datos sintéticos:** 5,040 observaciones, 6–7 días, resolución 10 min ✓ apto para prototipo
- **Datos reales:** 427 observaciones, máximo 9 días, resolución inconsistente ✗ insuficiente

**Problema:** Un modelo entrenado solo en datos sintéticos no funcionará en producción. La captura de Guadalajara puede complementarse con fuentes públicas internacionales para aprender patrones generales, pero la validación final seguirá requiriendo datos de Guadalajara.

## Nueva estrategia: datos reales multiciudad

No se exigirá que las fuentes externas sean mexicanas. Se priorizarán conjuntos públicos ya publicados con sensores reales y series temporales: METR-LA, PEMS-BAY, Caltrans PeMS y portales urbanos abiertos como Madrid. Estas fuentes sirven para preentrenamiento o comparación, no para afirmar que el comportamiento observado sea el de Guadalajara.

### Separación de funciones

```
Fuentes públicas externas -> aprender patrones generales
Datos disponibles de Guadalajara -> calibrar el contexto local
Datos nuevos de Guadalajara -> prueba final
Datos sintéticos -> pruebas técnicas, no validación real
```

### Requisito de compatibilidad

Antes de descargar o programar integraciones se elaborará una matriz por fuente con: ciudad, proveedor, licencia, periodo, resolución, sensores, variables, unidades, zona horaria, faltantes y formato. Una fuente se acepta si tiene al menos velocidad, timestamp fiable, resolución de 5–15 minutos y cobertura continua; flujo, ocupación, densidad y espera serán variables complementarias.

## Requisitos de datos reales

Para validar la hipótesis de anticipación de 18–20 minutos y crear un modelo operativo:

| Aspecto | Requisito | Actual | Estado |
|---------|-----------|--------|--------|
| Cobertura temporal | ≥30 días | máx. 9 días | ✗ Falta 21 días |
| Resolución | 5–15 minutos | inconsistente | ✗ No garantizado |
| Avenidas | ≥3 avenidas principales | 6–9 por fuente | ✓ Parcial |
| Variables | velocidad, densidad, flujo, espera, detenciones | presentes pero inconsistentes | ✓ Parcial |
| Continuidad | serie sin huecos significativos | fragmentada | ✗ Huecos documentados |

## Opciones de recolección

### Opción 1: Datasets públicos históricos internacionales

**Fuentes candidatas:** METR-LA, PEMS-BAY, Caltrans PeMS y portales urbanos de datos abiertos.

**Ventajas:** acceso sin trámite local, series temporales documentadas, sensores reales y formatos reutilizables.

**Desventajas:** diferencias de infraestructura, cobertura espacial, variables y metodología de medición.

**Uso:** preentrenamiento, comparación de patrones y validación de la portabilidad del modelo.

### Opción 2: Captura propia desde una fuente pública

Si un portal publica datos actuales pero no conserva histórico, se puede recolectar durante 30–90 días con un script propio. Cada captura debe conservar la respuesta original, timestamp de consulta, zona horaria, endpoint, estado HTTP y metadatos.

**Ventajas:** serie reproducible

**Desventajas:** solo genera histórico desde el inicio de la captura; no debe presentarse como histórico retrospectivo.

### Opción 3: Autoridades de tránsito municipal/estatal
**Fuente:** Secretaría de Movilidad, Instituto de Transporte y Vialidad, o equivalente local

**Cómo acceder:**
1. Solicitar datos abiertos o acceso API a los sistemas de monitoreo existentes
2. Especificar: avenidas principales (Chapultepec, México, Universidad, etc.), período (30 días), resolución (5–15 min)
3. Formatos típicos: CSV, JSON, consulta API

**Ventajas:** Datos reales, alta confiabilidad, variables estándar
**Desventajas:** Tramites administrativos, tiempo de respuesta, posibles restricciones de licencia
**Probabilidad:** Moderada (depende de políticas de datos abiertos locales)

### Opción 4: Plataformas de movilidad urbana
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

### Opción 5: Sensores IoT / cámaras de tráfico
**Fuente:** Sistemas de conteo de vehículos en campo

**Cómo acceder:**
1. Instalar sensores en intersecciones clave (costly)
2. Conectar a plataforma de recolección
3. Exportar datos después de 30 días de monitoreo

**Ventajas:** Datos de máxima precisión, control total
**Desventajas:** Muy costoso (€1,000–5,000 USD por sensor), tiempo de instalación
**Probabilidad:** Baja (impractible para proyecto académico)

### Opción 6: Datos históricos + simulación mejorada
**Fuente:** Extender datos actuales + mejorar modelo sintético

**Cómo acceder:**
1. Usar las 427 observaciones reales existentes para calibrar un modelo de simulación (SUMO, MATSim)
2. Generar 30 días simulados usando patrones de tráfico real observados
3. Usar sintéticos calibrados como aproximación

**Ventajas:** Bajo costo, control total, combina lo mejor de ambos mundos
**Desventajas:** Requiere experto en simulación, resultado sigue siendo "cuasi-sintético"
**Probabilidad:** Moderada

## Recomendación

**Prioridad 1 (inmediata):** descargar y verificar METR-LA y PEMS-BAY como fuentes públicas de transferencia.

**Prioridad 2:** evaluar el acceso gratuito a PeMS y revisar datasets históricos de Madrid u otros portales urbanos abiertos.

**Prioridad 3:** iniciar una captura propia desde una API o feed público que exponga datos actuales, manteniendo los originales y sus metadatos.

**Fallback:** usar datos sintéticos calibrados solo para prototipo académico y documentar que no validan el comportamiento real.

## Próximos pasos

Después de cerrar minería (documentar fuentes de definiciones):

1. **Semana 1:** Iniciar gestión de datos reales (Prioridad 1)
2. **Semana 2–4:** Ingeniería de datos (Fase 2) en paralelo
3. **Semana 4+:** Con datos reales en hand → pasar a análisis y modelado

**No iniciar transferencia ni afirmar validación hasta tener fuentes reales descargadas, documentadas y separadas por ciudad.**
