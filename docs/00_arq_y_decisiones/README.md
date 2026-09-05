# Arquitectura y decisiones del proyecto TSI

## 1. Propósito

Este documento define la arquitectura rectora del **Traffic Stability Index (TSI)**: una solución de inteligencia artificial de punta a punta para analizar tráfico urbano, detectar anomalías y estudiar señales de pre-colapso.

La arquitectura debe ser:

- **Coherente:** cada fase tiene una responsabilidad y un entregable.
- **Escalable:** permite aumentar fuentes, registros y usuarios sin rehacer el proyecto.
- **Mantenible:** separa datos, análisis, modelos, aplicación y operación.
- **Reproducible:** una ejecución debe poder repetirse con los mismos insumos y configuración.
- **Evolutiva:** comienza localmente y puede avanzar a nube sin cambiar el concepto del sistema.

## 2. Alcance

El sistema cubrirá estas fases:

1. Minería de datos.
2. Ingeniería de datos.
3. Base de datos SQL.
4. Análisis de datos.
5. Ciencia de datos y machine learning.
6. Interfaz mínima con Streamlit.
7. MLOps y despliegue progresivo.

La primera demostración será local con Streamlit. El despliegue en la nube se realizará después de estabilizar datos, SQL, modelos e interfaz.

## 3. Arquitectura por capas

```text
Fuentes
  |
  v
Minería de datos
  |
  v
Datos raw -> Procesamiento y validación -> Datos limpios
                                      |
                                      v
                              Base de datos SQL
                                      |
                    +-----------------+-----------------+
                    v                                   v
              Análisis y features                 Resultados ML
                    |                                   |
                    +-----------------+-----------------+
                                      v
                              Índice TSI versionado
                                      |
                                      v
                              Streamlit local
                                      |
                                      v
                              Despliegue en nube
                                      |
                                      v
                              Monitoreo MLOps
```

## 4. Responsabilidad de cada capa

### 4.1 Minería de datos

Define el problema y entiende las fuentes antes de transformar o modelar:

- Anomalía, congestión y pre-colapso.
- Calidad, cobertura y sesgos.
- Variables relevantes.
- Limitaciones de los datos.

**Salida:** diagnóstico y definición aprobada del problema.

### 4.2 Ingeniería de datos

Convierte fuentes heterogéneas en datos consistentes:

- Ingesta de fuentes.
- Normalización de nombres, tipos y fechas.
- Validación de rangos, duplicados y faltantes.
- Trazabilidad de origen y transformaciones.

**Salida:** datos procesados y reproducibles.

### 4.3 Base de datos SQL

Será la capa de consulta estructurada y persistencia operativa:

- Observaciones de tráfico.
- Avenidas y ubicaciones.
- Fuentes y cargas.
- Resultados de anomalías.
- Ejecuciones de modelos.
- Versiones del TSI.

Los archivos CSV seguirán funcionando como entrada, respaldo o intercambio; SQL será la fuente estructurada para análisis y aplicación cuando la fase esté implementada.

**Salida:** modelo relacional documentado y consultable.

### 4.4 Análisis de datos

Transforma los datos limpios en conocimiento:

- Estadísticas e indicadores.
- Patrones por avenida, fecha y horario.
- Relaciones entre velocidad, densidad, flujo y detenciones.
- Visualizaciones e interpretación.

**Salida:** hallazgos e indicadores analíticos.

### 4.5 Ciencia de datos

Construye y evalúa el componente inteligente:

- Características y ventanas temporales.
- DBSCAN, Isolation Forest y LOF.
- Métricas y criterios de comparación.
- Construcción y validación del TSI.
- Versionado de modelos, parámetros y resultados.

**Salida:** modelo seleccionado y TSI documentado.

### 4.6 Interfaz mínima

Streamlit será la primera capa de interacción:

- Indicadores principales.
- Filtros por avenida, fecha y método.
- Gráficas de comportamiento.
- Consulta de anomalías y TSI.
- Mensajes de carga, error y ausencia de datos.

La interfaz no debe contener lógica de limpieza o entrenamiento. Solo consulta servicios, archivos o funciones de una capa de aplicación definida.

**Salida:** demostración funcional para usuarios.

### 4.7 MLOps

Organiza la operación y evolución del sistema:

- Versionado de código, datos, modelos y configuración.
- Validaciones automáticas.
- Registro de experimentos.
- Ejecuciones reproducibles.
- Despliegue.
- Monitoreo de datos y desempeño.

**Salida:** sistema mantenible y preparado para crecer.

## 5. Flujo de datos y contratos

Cada fase debe entregar información verificable a la siguiente:

| Fase | Entrada | Salida | Criterio de aceptación |
|---|---|---|---|
| Minería | Fuentes y contexto | Definiciones, variables y riesgos | Problema delimitado |
| Ingeniería | Datos raw | Datos procesados y validados | Reglas de calidad cumplidas |
| SQL | Datos procesados | Tablas y relaciones | Consultas reproducibles |
| Análisis | Datos limpios/SQL | Indicadores y hallazgos | Resultados interpretables |
| Ciencia de datos | Features y etiquetas/reglas | Modelos y TSI | Evaluación documentada |
| Interfaz | Resultados aprobados | Vista Streamlit | Usuario puede consultar resultados |
| MLOps | Código, datos y modelos | Ejecución automatizada | Flujo repetible y observable |

No se debe avanzar de fase si la salida anterior no está definida y validada.

## 6. Organización del repositorio

```text
TSI/
├── data/                         # Datos por etapa del flujo
├── notebooks/                    # Exploración, investigación y prototipos
├── docs/                         # Decisiones y documentación de fases
│   ├── 00_arq_y_decisiones/
│   ├── 01_mineria_datos/
│   ├── 02_ingenieria_datos/sql/
│   ├── 03_analisis_datos/
│   ├── 04_ciencia_datos/
│   ├── 05_mlops/
│   └── 06_interfaz_minima/
├── streamlit_dashboard/          # Interfaz de demostración
└── .venv/                        # Entorno local, no es artefacto del sistema
```

Los notebooks sirven para investigación y validación. La lógica estable que se reutilice deberá separarse gradualmente de los notebooks para evitar duplicación y facilitar pruebas.

## 7. Entornos de evolución

### Entorno actual: local

- Archivos CSV existentes.
- Notebooks.
- Entorno virtual `.venv`.
- SQL local cuando se implemente.
- Streamlit local para demostración.

### Entorno posterior: nube

Se evaluará después de estabilizar el sistema local:

- Almacenamiento de datos.
- Base SQL administrada o servidor SQL.
- Ejecución programada del pipeline.
- Aplicación Streamlit desplegada.
- Monitoreo y registro.

La nube es una evolución de infraestructura, no una condición para validar la arquitectura.

## 8. Decisiones iniciales

| Decisión | Motivo |
|---|---|
| Mantener el flujo por etapas | Evita mezclar datos raw, limpios y resultados |
| Usar SQL como capa estructurada | Permite consultas, relaciones y trazabilidad |
| Mantener Streamlit como primera interfaz | Permite demostrar el sistema sin crear un frontend complejo |
| Separar notebooks de la aplicación | Reduce acoplamiento y facilita mantenimiento |
| Empezar localmente | Permite validar el diseño antes de operar en nube |
| Documentar antes de implementar cada fase | Reduce retrabajo y decisiones contradictorias |

## 9. Escalabilidad y mantenimiento

- Usar identificadores, fechas y nombres de fuente consistentes.
- Evitar rutas absolutas en notebooks y aplicación.
- Separar configuración de lógica.
- No sobrescribir datos raw.
- Registrar versiones de datasets y modelos.
- Diseñar consultas SQL reutilizables.
- Mantener la interfaz desacoplada del entrenamiento.
- Validar cambios antes de incorporarlos a la siguiente fase.
- Preferir componentes simples hasta que el volumen o la operación justifiquen mayor complejidad.

## 10. Orden de implementación

1. Aprobar esta arquitectura y el alcance.
2. Completar la minería de datos.
3. Diseñar el pipeline de ingeniería de datos.
4. Diseñar el esquema SQL.
5. Consolidar análisis e indicadores.
6. Formalizar evaluación, modelos y TSI.
7. Definir e implementar la interfaz mínima.
8. Preparar prácticas MLOps.
9. Demostrar localmente con Streamlit.
10. Evaluar despliegue en nube.

## 11. Criterio de cierre de arquitectura

La arquitectura se considera suficientemente definida cuando:

- El flujo entre fases está claro.
- Cada fase tiene entrada, salida y criterio de aceptación.
- SQL, Streamlit y MLOps tienen una responsabilidad delimitada.
- Se distingue el estado actual de la evolución futura.
- Las decisiones importantes quedan registradas aquí o en documentos enlazados.

Este documento puede evolucionar, pero cualquier cambio estructural debe registrarse como una nueva decisión y explicar su motivo.
