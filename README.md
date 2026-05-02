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
2. Procesamiento y limpieza de datos para garantizar calidad. 🔄 **EN CURSO**
3. Análisis exploratorio para identificar patrones y relaciones entre variables. 🔄 **EN CURSO**
4. Construcción de modelos para representar el comportamiento del sistema y evaluar la hipótesis.
5. Validación de resultados mediante comparación con datos reales.

## 9b. Fase de procesamiento y análisis (Siguiente etapa detallada)

### ¿Qué haremos a continuación?

Ahora que contamos con **117 registros reales** de tráfico de Guadalajara, pasaremos a la fase crítica de **transformación de datos en información**. Esta etapa es fundamental para identificar patrones, anomalías y relaciones entre variables que nos permitan construir la métrica TSI.

### Pasos específicos del procesamiento:

#### **1. Limpieza y validación de datos**
- Detectar y tratar valores faltantes (NaN, nulos)
- Identificar y manejar valores atípicos (outliers) que podrían distorsionar el análisis
- Validar rangos de variables (ej: velocidad no puede ser negativa)
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

## 12. Estado del proyecto (Actualizado: 1 de mayo de 2026)

### Fase actual: **Procesamiento, limpieza y análisis exploratorio de datos** 🔄

#### ✅ Fase completada: Recopilación
- **117 registros** de tráfico con patrones realistas de Guadalajara
- Coordenadas geográficas exactas (Google Maps / OpenStreetMap)
- 5 franjas horarias con patrones de tráfico realistas
- Datos listos en: `data/raw/traffic_data.csv`

#### 🔄 Fase actual: Procesamiento en 4 notebooks secuenciales

##### **Notebook 1: Data_Quality_Assessment.ipynb**
Diagnóstico inicial de calidad
- Detectar valores nulos y faltantes
- Identificar tipos de datos incorrectos
- Validar rangos de valores
- Detectar duplicados y outliers
- **Salida**: Reporte de problemas encontrados

##### **Notebook 2: Data_Cleaning.ipynb**
Transformación y corrección de datos
- Conversión de tipos de datos (timestamp → datetime)
- Imputación de valores nulos (por media de avenida)
- Remoción de duplicados
- Tratamiento de outliers (clipping)
- Validación y corrección de rangos
- Limpieza de columnas categóricas
- **Salida**: Dataset limpio en `data/processed/traffic_data_clean.csv`

##### **Notebook 3: Data_Validation.ipynb**
Verificación de integridad post-limpieza
- Validar estructura de datos
- Verificar completitud (0 valores nulos)
- Confirmar tipos de datos
- Validar rangos de todas las variables
- Confirmar ausencia de duplicados
- Verificar consistencia referencial (avenidas válidas)
- Integridad temporal
- **Salida**: Dataset validado y listo para análisis

##### **Notebook 4: Exploratory_Data_Analysis.ipynb** 
Descubrimiento de patrones e insights
- Estadísticas descriptivas por avenida
- Análisis de distribuciones (velocidad, densidad, detenciones)
- Correlación entre variables (matriz de correlación)
- Clasificación de estados de tráfico (Flujo Libre → Congestión Severa)
- Identificación de condiciones de pre-colapso
- Visualizaciones (boxplots, heatmaps, scatter plots)
- Avenidas críticas (con mayor congestión)
- **Salida**: Insights y gráficos para feature engineering

#### 📊 Estructura de procesamiento
```
data/
├── raw/
│   ├── traffic_data.csv (datos originales - 117 registros)
│   └── scraped_traffic.csv
│
└── processed/
    ├── traffic_data_clean.csv (datos limpios)
    ├── traffic_data_with_classifications.csv (con estados)
    ├── estadisticas_por_avenida.csv (análisis)
    └── [visualizaciones EDA]
```

#### 🎯 Flujo de ejecución recomendado
```
1. Ejecutar: 01_Data_Quality_Assessment.ipynb
   ↓ Identifica problemas
   
2. Ejecutar: 02_Data_Cleaning.ipynb
   ↓ Corrige problemas
   
3. Ejecutar: 03_Data_Validation.ipynb
   ↓ Verifica correcciones
   
4. Ejecutar: 04_Exploratory_Data_Analysis.ipynb
   ↓ Descubre patrones
   
5. Feature Engineering (próximo)
   ↓ Crea variables predictivas
   
6. Construcción de métrica TSI
   ↓ Implementa modelo
   
7. Validación y predicción
```

#### 📈 Insights esperados del EDA
- Correlación entre velocidad y densidad
- Identificación de avenidas críticas
- Patrones horarios de congestión
- Combinaciones de variables que predicen pre-colapso
- Distribución de estados de tráfico
- Ventana de tiempo anticipada para alertas

#### 🔄 Próximos pasos después de EDA
1. **Feature Engineering** - Crear variables dinámicas
2. **Construcción de TSI** - Métrica de estabilidad
3. **Validación** - Pruebas de predictibilidad
4. **Implementación** - Sistema en tiempo real
