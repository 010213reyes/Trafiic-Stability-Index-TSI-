# Fase 06: Interfaz Streamlit

Esta fase documenta la interfaz de presentacion de la investigacion internacional. El codigo ejecutable permanece en `streamlit_dashboard/app.py` porque esa es la ruta configurada para Streamlit Community Cloud.

## Responsabilidad

- mostrar resultados analiticos ya generados;
- presentar fuentes, cobertura, calidad y estado SQL;
- evitar cargar datasets grandes completos en la interfaz;
- separar presentacion de procesamiento y modelado.

## Entrada actual

La aplicacion consume contratos, metadatos, muestras Parquet y salidas ligeras de `data/03_analysis_output/` cuando estan disponibles.

## Ejecucion local

```powershell
streamlit run streamlit_dashboard/app.py
```

No se debe ejecutar con `python streamlit_dashboard/app.py`, porque Streamlit necesita iniciar el servidor mediante su comando `streamlit run`.
