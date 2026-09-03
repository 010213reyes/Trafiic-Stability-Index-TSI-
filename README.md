# Traffic Stability Index (TSI)

## 1. Motivación del proyecto

Guadalajara es una ciudad en constante crecimiento, donde el tráfico se ha convertido en una de las principales problemáticas urbanas. Existen avenidas que, para los conductores locales, representan puntos críticos en determinados momentos del día, caracterizados por tiempos de espera elevados, congestión impredecible y una carga constante de estrés.

La mayoría de los enfoques tradicionales analizan el tráfico una vez que la congestión ya está presente, describiendo el fenómeno en lugar de anticiparlo. Este proyecto surge a partir de una inquietud distinta: comprender si el tráfico puede ser interpretado como un sistema dinámico cuyo comportamiento previo al colapso puede ser identificado mediante datos.

## 2. Planteamiento del problema

El tráfico no colapsa de forma instantánea. Antes de alcanzar un estado crítico, el sistema atraviesa una serie de transiciones en las que variables como la velocidad, la densidad vehicular y el flujo comienzan a deteriorarse progresivamente. Estas variaciones no siempre son evidentes a simple vista, pero pueden contener información relevante sobre el comportamiento futuro del sistema.

Bajo esta perspectiva, el problema se redefine no como la medición del congestionamiento, sino como la identificación de condiciones previas que indican que el sistema está perdiendo estabilidad.

## 3. Hipótesis del proyecto

### H1 (hipótesis alternativa)

Es posible identificar un estado previo al colapso del tráfico urbano mediante el análisis conjunto de variables operativas del sistema. Este estado, definido como **zona de pre-colapso**, puede ser detectado con suficiente anticipación para inferir la probabilidad de que ocurra congestión en un intervalo corto de tiempo, estimado entre **3 y 10 minutos**.

### H0 (hipótesis nula)

No existe un patrón consistente o detectable que permita anticipar el colapso del tráfico de manera confiable a partir de las variables observadas.

## 4. Objetivo

Desarrollar un modelo basado en datos que permita identificar condiciones de riesgo dentro del sistema de tráfico urbano y anticipar eventos de congestión antes de que estos ocurran.

Como parte del desarrollo, se busca definir una representación cuantitativa del estado del sistema que permita interpretar su estabilidad en distintos momentos.

De forma paralela, el proyecto contempla la construcción de una **métrica propia** que integre múltiples variables del sistema en una sola expresión. Esta métrica se fundamentará en relaciones matemáticas entre velocidad, densidad, flujo y frecuencia de detenciones, con el propósito de capturar el comportamiento dinámico del tráfico y proporcionar una medida interpretable del riesgo de colapso.

## 5. Enfoque del proyecto

El proyecto se desarrolla como una integración entre análisis de datos, modelado predictivo e interpretación del comportamiento de sistemas dinámicos. No se limita a describir patrones, sino que busca entender la lógica interna del sistema de tráfico y cómo pequeñas variaciones pueden escalar hasta generar eventos de congestión.

A lo largo del proceso, el análisis se acompaña de una narrativa técnica que permite traducir los hallazgos en interpretaciones comprensibles, manteniendo un equilibrio entre rigor matemático y claridad conceptual.

## 6. Definiciones conceptuales

- **Colapso:** estado en el que el sistema pierde eficiencia operativa, reflejado en una reducción significativa de la velocidad promedio y en una disminución del flujo efectivo de vehículos.
- **Zona de pre-colapso:** intervalo previo al estado crítico, en el cual el sistema aún funciona, pero presenta señales de inestabilidad.
- **Capacidad anticipatoria:** habilidad del modelo para identificar condiciones de riesgo antes de que ocurra el colapso, permitiendo una interpretación prospectiva del sistema.

## 7. Variables del modelo

El análisis considera variables operativas del sistema de tráfico como:

- Velocidad promedio
- Densidad vehicular
- Flujo
- Tiempo de espera
- Frecuencia de detenciones
- Variables contextuales (hora del día y características específicas de las avenidas)

## 8. Construcción de la métrica

Se plantea la construcción de una métrica que permita representar el estado del sistema en términos cuantitativos, integrando múltiples dimensiones del tráfico en una sola variable capaz de reflejar su nivel de estabilidad.

Desde un punto de vista matemático, la formulación se basa en la relación entre variables que, en conjunto, describen el comportamiento del sistema. Por ejemplo, una disminución en la velocidad acompañada de un incremento en la densidad y en la frecuencia de detenciones puede interpretarse como una señal de deterioro.

La validez de esta métrica dependerá de:

- Su capacidad para correlacionarse con eventos reales de congestión.
- Su consistencia a lo largo de distintos escenarios.

## 9. Enfoque metodológico

El proyecto sigue un proceso estructurado:

1. Recolección de datos relevantes del sistema de tráfico. ✅ **COMPLETADO**
2. Procesamiento y limpieza de datos para garantizar calidad. ✅ **COMPLETADO**
3. Análisis exploratorio para identificar patrones y relaciones entre variables. ✅ **COMPLETADO**
4. Construcción de modelos para representar el comportamiento del sistema y evaluar la hipótesis. ✅ **COMPLETADO**
5. Validación de resultados mediante comparación con datos reales. ✅ **COMPLETADO**

## 9b. Fase de procesamiento y análisis (Investigación concluida)

- Estandarizar formatos de fechas y tipos de datos
- **Resultado esperado**: Dataset limpio y consistente sin ruido

#### **2. Análisis exploratorio de datos (EDA)**
- Generar estadísticas descriptivas por avenida y franja horaria
- Visualizar distribuciones de velocidad, densidad y detenciones
- Identificar patrones temporales (¿cuándo es más congestionado?)
- Detectar relaciones entre variables (correlación entre densidad y velocidad)
- Crear perfiles de tráfico por avenida
- **Resultado esperado**: Comprensión profunda del comportamiento del tráfico

#### **3. Ingeniería de características (Feature Engineering)**
- Crear variables derivadas que capturen comportamientos dinámicos:
  - **Tasa de cambio de velocidad**: ¿qué tan rápido disminuye la velocidad?
  - **Índice de congestión relativa**: comparar densidad actual vs. histórica
  - **Propensión a detenciones**: relación entre densidad y frecuencia de paradas
  - **Suavidad del flujo**: variabilidad de velocidad en ventanas de tiempo
- Normalizar variables para comparabilidad
- **Resultado esperado**: Variables que representen dinámicas de pre-colapso

#### **4. Identificación de patrones y correlaciones**
- Determinar qué variables se correlacionan más fuertemente con congestión
- Identificar combinaciones de variables que actúan como "señales de alerta"
- Análisis de series temporales para detectar tendencias
- Segmentación de datos por escenarios (horas pico, normales, off-peak)
- **Resultado esperado**: Comprensión de los mecanismos que predicen colapso

#### **5. Construcción de la métrica TSI (Traffic Stability Index)**
- Formular una ecuación matemática que integre múltiples variables
- Basar la métrica en relaciones causales identificadas en los datos
- Calibrar pesos de cada componente según su poder predictivo
- Validar que la métrica sea interpretable (escala 0-100, por ejemplo)
- **Resultado esperado**: Métrica única que resume el estado de estabilidad del tráfico

#### **6. Validación y refinamiento**
- Probar la métrica en datos históricos para verificar su capacidad predictiva
- Ajustar parámetros según desempeño
- Documentar limitaciones y casos especiales
- **Resultado esperado**: Métrica robusta y confiable

### ¿Por qué es importante esta fase?

La calidad del análisis depende directamente de la calidad de los datos y la claridad de los patrones identificados. Sin una limpieza y exploración adecuada:
- No podremos confiar en las relaciones identificadas
- La métrica TSI podría captar ruido en lugar de señales reales
- Los modelos predictivos serían poco confiables

### ¿Qué esperamos descubrir?

- **Relaciones clave**: Qué combinación de factores predice mejor un colapso
- **Ventana de anticipación**: Cuánto tiempo antes de un colapso son detectables las señales
- **Avenidas críticas**: Cuáles tienen mayor variabilidad y riesgo de congestión
- **Patrones horarios**: Cuándo y dónde es más probable la inestabilidad

---

## 10. Impacto esperado

El proyecto tiene el potencial de aportar una nueva perspectiva en la interpretación del tráfico urbano, al pasar de un enfoque reactivo a uno anticipatorio. Identificar condiciones de riesgo antes de que se manifiesten en forma de congestión abre la puerta a aplicaciones prácticas orientadas a la toma de decisiones, tanto a nivel individual como colectivo.

Más allá de los resultados técnicos, el valor del proyecto radica en su capacidad para transformar datos en información útil, permitiendo una mejor comprensión de un fenómeno cotidiano que afecta directamente la calidad de vida de las personas.

## 11. Enfoque humano

Aunque el proyecto se fundamenta en datos y modelos matemáticos, su origen y propósito están ligados a la experiencia diaria de los conductores. El tráfico no es únicamente un problema técnico, sino una situación que impacta el tiempo, el estado emocional y la rutina de miles de personas.

En este sentido, el análisis busca mantener una conexión con el contexto real en el que se desarrolla, utilizando el lenguaje de los datos para interpretar una experiencia humana común y convertirla en conocimiento estructurado.

---

## 12. Estado del proyecto (Actualizado: 3 de septiembre de 2026)

### Fase actual: **Investigación concluida y planificación de implementación** ✅

#### ✅ Avances confirmados
- Estructura de datos migrada a esquema por etapas (`00_raw`, `01_processed`, `02_clean`, `03_algorithm_output`).
- EDA principal estabilizado en `04_Exploratory_Data_Analysis_TSI.ipynb`.
- Notebook independiente de Isolation Forest creado y validado: `05_Isolation_Forest_TSI.ipynb`.
- Notebook independiente de Local Outlier Factor creado y validado: `06_Local_Outlier_Factor_TSI.ipynb`.
- Notebook independiente de DBSCAN creado y validado: `07_DBSCAN_TSI.ipynb`.
- Notebook de cierre comparativo y formulación final del índice validado: `08_Algorithm_Comparison_and_TSI.ipynb`.
- Dataset filtrado generado por Isolation Forest en `data/02_clean/filtered_isolation_forest.csv`.
- Dataset filtrado generado por Local Outlier Factor en `data/02_clean/filtered_local_outlier_factor.csv`.
- Dataset filtrado generado por DBSCAN en `data/02_clean/filtered_dbscan.csv`.
- Visualizaciones de algoritmo exportadas en `data/03_algorithm_output/`.

#### 📁 Estructura actual de datos (resumen)
```
data/
├── 00_raw/
│   ├── traffic_data.csv
│   ├── scraped_traffic.csv
│   ├── synthetic_traffic.csv
│   ├── crowdsourcing_raw.csv
│   └── crowdsourcing_aggregated.csv
├── 01_processed/
├── 02_clean/
│   ├── traffic_data.csv
│   ├── traffic_enriched.csv
│   ├── historical_consolidated.csv
│   ├── filtered_isolation_forest.csv
│   ├── filtered_local_outlier_factor.csv
│   └── filtered_dbscan.csv
└── 03_algorithm_output/
```

#### 📓 Estado de notebooks en procesamiento/modelado
- `00_Algorithm_Evaluation_Pipeline.ipynb`: evaluación comparativa de enfoques.
- `01_Data_Quality_Assessment.ipynb`: diagnóstico de calidad.
- `02_Data_Cleaning.ipynb`: limpieza y normalización.
- `03_Data_Validation.ipynb`: validación posterior a limpieza.
- `04_Exploratory_Data_Analysis_TSI.ipynb`: EDA consolidado para interpretación del sistema.
- `05_Isolation_Forest_TSI.ipynb`: flujo completo por algoritmo (diagnóstico, entrenamiento, filtrado y salidas).
- `06_Local_Outlier_Factor_TSI.ipynb`: flujo completo por algoritmo (diagnóstico, entrenamiento, filtrado y salidas).
- `07_DBSCAN_TSI.ipynb`: flujo completo por algoritmo (diagnóstico, búsqueda de parámetros, filtrado y salidas).
- `08_Algorithm_Comparison_and_TSI.ipynb`: cierre comparativo y definición final del TSI unificado.

#### 📘 Demostración técnica
- `03_Demostracion_Tecnica_TSI/01_Demostracion_Tecnica_TSI.ipynb`: ejemplo técnico único para mostrar el proyecto de principio a fin con los artefactos finales.

#### 🎯 Flujo recomendado de consulta
```
1. 01_Data_Quality_Assessment.ipynb
2. 02_Data_Cleaning.ipynb
3. 03_Data_Validation.ipynb
4. 04_Exploratory_Data_Analysis_TSI.ipynb
5. 05_Isolation_Forest_TSI.ipynb
6. 06_Local_Outlier_Factor_TSI.ipynb
7. 07_DBSCAN_TSI.ipynb
8. 08_Algorithm_Comparison_and_TSI.ipynb
9. 03_Demostracion_Tecnica_TSI/01_Demostracion_Tecnica_TSI.ipynb
10. streamlit_dashboard/app.py
```

#### 🔄 Próximos pasos inmediatos
1. Diseñar la arquitectura de datos y la base de datos SQL.
2. Definir el pipeline reproducible de ingeniería de datos.
3. Planificar la integración del modelo con la interfaz Streamlit.

#### 🖥️ Capa de visualización
- `streamlit_dashboard/README.md`: guía de la interfaz ejecutiva y fuentes de datos que consumirá.
- `streamlit_dashboard/app.py`: punto de entrada del dashboard ejecutivo.
- `streamlit_dashboard/`: carpeta separada para dashboards y pantallas de decisión.

---
## 13. Artefactos y puntos de consulta

### Resultados principales
- [notebooks/02_Data_Processing/08_Algorithm_Comparison_and_TSI.ipynb](notebooks/02_Data_Processing/08_Algorithm_Comparison_and_TSI.ipynb): comparación homogénea de algoritmos y cierre de TSI.
- [notebooks/03_Demostracion_Tecnica_TSI/01_Demostracion_Tecnica_TSI.ipynb](notebooks/03_Demostracion_Tecnica_TSI/01_Demostracion_Tecnica_TSI.ipynb): demostración técnica resumida del flujo completo.
- [streamlit_dashboard/app.py](streamlit_dashboard/app.py): panel ejecutivo con la narrativa final del proyecto.
- [streamlit_dashboard/README.md](streamlit_dashboard/README.md): guía de la capa de visualización.

### Datos de salida relevantes
- `data/02_clean/filtered_isolation_forest.csv`
- `data/02_clean/filtered_local_outlier_factor.csv`
- `data/02_clean/filtered_dbscan.csv`
- `data/03_algorithm_output/`

### Ruta de consulta recomendada
1. Revisión de datos base en `data/02_clean/traffic_enriched.csv`.
2. Lectura de comparación en `notebooks/02_Data_Processing/08_Algorithm_Comparison_and_TSI.ipynb`.
3. Consulta de salidas visuales en `data/03_algorithm_output/`.
4. Navegación ejecutiva en `streamlit_dashboard/app.py`.

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

