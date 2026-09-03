---

## 14. Nueva hoja de ruta de implementación

Con la investigación terminada, el proyecto avanzará hacia una solución de inteligencia artificial de punta a punta.

### Fase 1: Minería de datos

- Formalizar las definiciones de anomalía, congestión y pre-colapso.
- Documentar las fuentes disponibles, su calidad y sus limitaciones.
- Consolidar los hallazgos obtenidos durante la investigación.

**Entregable:** definición funcional del problema y catálogo de datos.

### Fase 2: Ingeniería de datos

- Diseñar el flujo `raw -> processed -> clean`.
- Estandarizar formatos, tipos y reglas de calidad.
- Registrar el origen y las transformaciones de cada conjunto.
- Preparar cargas reproducibles hacia SQL.

**Entregable:** pipeline reproducible y reglas de validación.

### Fase 3: Base de datos SQL

- Centralizar observaciones, avenidas, fuentes, ejecuciones y resultados.
- Definir tablas, claves, relaciones e índices.
- Separar datos originales, procesados y resultados de modelos.
- Permitir consultas desde la aplicación.

**Entregable:** modelo relacional documentado y base SQL funcional.

### Fase 4: Análisis de datos

- Convertir los hallazgos en indicadores operativos.
- Analizar resultados por avenida, periodo y franja horaria.
- Mantener visualizaciones orientadas a interpretación y decisiones.

**Entregable:** indicadores y reportes analíticos.

### Fase 5: Ciencia de datos y machine learning

- Consolidar variables y características del modelo.
- Comparar DBSCAN, Isolation Forest y LOF con criterios definidos.
- Validar el TSI y documentar su interpretación y limitaciones.
- Versionar modelos, parámetros, datos y métricas.

**Entregable:** modelo seleccionado, TSI validado y evaluación documentada.

### Fase 6: Interfaz mínima

- Usar Streamlit como interfaz de demostración.
- Mostrar indicadores, gráficas y anomalías relevantes.
- Incorporar filtros por avenida, fecha y método.
- Consultar resultados almacenados en SQL.
- Incluir estados claros de carga, error y ausencia de datos.

**Entregable:** demostración funcional para usuarios y presentación del proyecto.

### Fase 7: MLOps

- Versionar código, datos, modelos y configuraciones.
- Automatizar pruebas de calidad y validación.
- Registrar experimentos y métricas.
- Preparar entrenamiento y actualización reproducibles.
- Monitorear calidad de datos y desempeño del modelo.

**Entregable:** flujo operativo preparado para mantenimiento y evolución.

### Estrategia de despliegue

La primera demostración se realizará localmente con Streamlit. El despliegue en la nube será una etapa posterior, cuando la arquitectura, la base SQL, el pipeline y el modelo estén estabilizados.


Fuentes -> Pipeline -> SQL -> Análisis y ML -> TSI -> Streamlit -> Nube
```

### Orden de implementación

1. Arquitectura y catálogo de datos.
2. Pipeline de ingeniería de datos.
3. Diseño e integración de SQL.
4. Evaluación final del modelo y del TSI.
5. Interfaz Streamlit para demostración.
6. Automatización y prácticas MLOps.
7. Despliegue en la nube.