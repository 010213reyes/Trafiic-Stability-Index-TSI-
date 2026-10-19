# TSI: investigacion internacional de trafico

Este repositorio contiene la investigacion nueva del Traffic Stability Index (TSI), con Guadalajara como ciudad objetivo de calibracion y validacion.

## Arquitectura

```text
Fuentes externas
  -> data/00_raw/external
  -> data/01_processed
  -> data/02_clean/external y consolidated
  -> docs/02_ingenieria_datos/sql
  -> docs/03_analisis_datos
  -> docs/04_ciencia_datos
  -> streamlit_dashboard
```

## Rutas principales

- `docs/`: documentacion canonica de la investigacion.
- `data/00_raw/external/`: fuentes externas originales.
- `data/01_processed/`: datos procesados y metadatos de linaje.
- `data/02_clean/external/`: fuentes limpias por ciudad o proveedor.
- `data/02_clean/consolidated/`: consolidado internacional para analisis y SQL.
- `scripts/`: procesamiento internacional y perfiles reproducibles.
- `notebooks/03_Analisis_Datos/`: exploracion documentada.
- `streamlit_dashboard/`: interfaz de la investigacion nueva.

## Flujo de trabajo

1. Revisar `docs/01_mineria_datos/`.
2. Ejecutar y validar la ingenieria documentada en `docs/02_ingenieria_datos/`.
3. Analizar el consolidado desde `docs/03_analisis_datos/`.
4. Validar resultados en MySQL despues de completar la carga.
5. Consumir resultados desde Streamlit.

Los datasets grandes, resultados generados, credenciales y configuracion local no se publican en Git.
