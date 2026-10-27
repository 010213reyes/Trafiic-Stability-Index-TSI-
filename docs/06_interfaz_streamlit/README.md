# Fase 06: Interfaz Streamlit

Esta fase documenta y organiza la interfaz de presentacion de la investigacion internacional. El codigo ejecutable permanece en `streamlit_app/`, porque `streamlit_app/app.py` es la ruta de entrada configurada para Streamlit Community Cloud.

## Responsabilidad

- presentar el recorrido animado desde mineria hasta MLOps;
- ofrecer una ventana de navegacion independiente para cada fase;
- mostrar resultados analiticos ya generados;
- presentar fuentes, cobertura, calidad, TSI, modelos y estado SQL;
- evitar cargar datasets grandes completos en la interfaz;
- separar presentacion de procesamiento y modelado.

## Estructura de la implementacion

```text
streamlit_app/
├── app.py                 # entrada, autenticacion y navegacion
├── config.py              # rutas y lectores de artefactos
├── components.py          # estilos, animacion y navegacion comun
└── views/
	├── home.py            # mapa animado del proyecto
	├── mineria.py
	├── ingenieria.py
	├── analisis.py
	├── ciencia.py
	└── mlops.py
```

La pantalla inicial representa el flujo `Mineria -> Ingenieria -> Analisis -> Ciencia de datos -> MLOps`. Cada fase tiene su propia vista, controles anterior/siguiente y acceso desde la barra lateral. Las animaciones representan artefactos ya generados; no simulan entrenamiento en tiempo real.

## Entradas actuales

La aplicacion consume contratos, metadatos de calidad, muestras Parquet, resultados de ciencia de datos y salidas MLOps. Los datasets grandes no se cargan completos en la interfaz.

## Ejecucion local

```powershell
streamlit run streamlit_app/app.py
```

No se debe ejecutar con `python streamlit_app/app.py`, porque Streamlit necesita iniciar el servidor mediante su comando `streamlit run`.
