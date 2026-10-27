# Dashboard internacional TSI

Esta carpeta contiene la interfaz modular de la investigacion internacional nueva.

La pantalla inicial presenta un recorrido animado por las fases de mineria, ingenieria, analisis, ciencia de datos y MLOps. Cada fase se implementa en una vista separada dentro de `views/`.

## Entrada

El punto de entrada es `app.py`. La aplicacion consulta contratos, metadatos de calidad, el consolidado internacional, resultados cientificos y artefactos MLOps.

La estructura principal es:

```text
app.py          # entrada y navegacion
config.py       # rutas y lectores
components.py   # estilos, animaciones y controles compartidos
views/          # una ventana por fase
```

## Regla de datos

Los datasets grandes y las credenciales permanecen fuera de Git. La aplicacion debe trabajar con muestras, metadatos o conexiones configuradas localmente.

## Ejecucion local

Desde la raiz del proyecto:

```powershell
streamlit run streamlit_app/app.py
```

La documentacion funcional y las decisiones de interfaz se mantienen en `docs/06_interfaz_streamlit/`.
