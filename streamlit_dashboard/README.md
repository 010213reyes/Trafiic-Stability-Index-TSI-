# Dashboard internacional TSI

Esta carpeta contiene la interfaz de la investigacion internacional nueva.

## Entrada

El punto de entrada es `app.py`. La aplicacion consulta contratos, metadatos de calidad, el consolidado internacional y el estado de la carga SQL.

## Regla de datos

Los datasets grandes y las credenciales permanecen fuera de Git. La aplicacion debe trabajar con muestras, metadatos o conexiones configuradas localmente.

## Ejecucion local

Desde la raiz del proyecto:

```powershell
streamlit run streamlit_dashboard/app.py
```

La documentacion funcional y las decisiones de interfaz se mantienen en `docs/06_interfaz_streamlit/`.
