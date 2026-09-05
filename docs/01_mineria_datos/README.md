# Fase 1: Minería de datos

## Objetivo

Definir con precisión el problema del TSI antes de construir nuevos pipelines o modelos: qué es una anomalía, qué es congestión, qué significa pre-colapso y qué variables pueden representar esos estados.

## Alcance inicial

Esta fase no requiere servicios ni nuevas APIs. Se trabajará primero con:

- `data/00_raw/` del proyecto.
- Resultados y notebooks existentes.
- Fuentes públicas y documentación.
- Herramientas locales ya disponibles en `.venv`.

## Preguntas de investigación

1. ¿Cómo se define congestión con las variables disponibles?
2. ¿Qué diferencia existe entre un valor atípico, una anomalía y un evento de pre-colapso?
3. ¿Qué variables tienen sentido operativo para detectar inestabilidad?
4. ¿Qué sesgos tienen los datos sintéticos, históricos, scraped y crowdsourcing?
5. ¿Qué calidad, cobertura temporal y cobertura por avenida tiene cada fuente?
6. ¿Qué evidencia permite evaluar la hipótesis de anticipación de 3 a 10 minutos?

## Fuentes abiertas para comenzar

### Metodología y minería de datos

- [IBM: metodología CRISP-DM](https://www.ibm.com/docs/en/spss-modeler/saas?topic=overview-crisp-dm)
- [IBM: introducción a la minería de datos](https://www.ibm.com/topics/data-mining)
- [NIST: Data Quality](https://www.nist.gov/data-quality)

### Tráfico y datos públicos

- [INEGI: vehículos de motor registrados](https://www.inegi.org.mx/temas/vehiculos/)
- [Datos Abiertos del Gobierno de México](https://datos.gob.mx/)
- [Datos Abiertos Jalisco](https://datos.jalisco.gob.mx/)
- [FHWA: conceptos y medición del tráfico](https://ops.fhwa.dot.gov/publications/fhwahop08054/)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/)
- [OpenML: conjuntos de datos y experimentos](https://www.openml.org/)

## Qué registrar durante la investigación

Para cada fuente o definición, registrar:

- Enlace y fecha de consulta.
- Concepto que aporta.
- Variables relacionadas.
- Cobertura geográfica y temporal.
- Limitaciones y posibles sesgos.
- Decisión tomada para el proyecto.

## Entregables de esta fase

- `01_definiciones.md`: anomalía, congestión, pre-colapso y capacidad anticipatoria.
- `02_catalogo_fuentes.md`: inventario de fuentes y calidad inicial.
- `03_variables_relevantes.md`: variables candidatas y justificación.
- `04_riesgos_y_sesgos.md`: sesgos, limitaciones y riesgos de interpretación.
- `05_diagnostico_final.md`: diagnóstico y definición aprobada del problema.

## Criterio de cierre

La fase termina cuando exista una definición aprobada del problema, un catálogo de fuentes, una lista justificada de variables y un registro explícito de limitaciones. Todavía no se deben modificar modelos ni crear infraestructura SQL.

## Estrategia de trabajo eficiente

1. Usar primero los datos existentes antes de recolectar nuevos.
2. Preferir fuentes públicas descargables y evitar consultas innecesarias.
3. Investigar y documentar antes de entrenar modelos.
4. Ejecutar análisis localmente en el entorno `.venv`.


## Prompt para otro agente

```text
Estamos comenzando la Fase 1: Minería de datos del proyecto Traffic Stability Index (TSI), enfocado en detectar anomalías, congestión y señales de pre-colapso en el tráfico urbano de Guadalajara.

Por ahora no escribas código, no modifiques archivos y no instales paquetes. Realiza únicamente investigación y planeación usando fuentes abiertas y los datos que ya existen en data/00_raw/ y en los notebooks del proyecto.

Necesito que analices:

1. Definiciones operativas de anomalía, congestión y pre-colapso.
2. Calidad, cobertura, origen y limitaciones de cada fuente de datos.
3. Variables disponibles y variables relevantes para el problema.
4. Diferencia entre outlier estadístico, anomalía operativa y evento de congestión.
5. Sesgos de datos sintéticos, históricos, scraped y crowdsourcing.
6. Viabilidad de detectar señales con una anticipación de 3 a 10 minutos.

Entrega un informe breve con:

- Diagnóstico del problema.
- Tabla de fuentes y calidad.
- Definiciones recomendadas para el TSI.
- Variables candidatas y justificación.
- Riesgos, sesgos y limitaciones.
- Preguntas que deben resolverse antes de pasar a ingeniería de datos.
- Referencias con enlaces y fecha de consulta.

No inventes datos ni afirmes que existe capacidad predictiva sin evidencia. Distingue siempre entre lo observado en los archivos y lo recomendado por la literatura. Prioriza fuentes abiertas y evita trabajo exploratorio innecesario.
```
