# 01 Versionado del modelo

Registra el modelo seleccionado, sus parámetros, métricas, versión de datos, configuración y hash de los artefactos relevantes.

## Entregables

- modelo serializado;
- manifiesto de versión;
- métricas de entrenamiento y evaluación;
- evidencia de procedencia y compatibilidad.

## Ejecución

Desde la raíz del proyecto:

```powershell
.venv\Scripts\python.exe docs\05_mlops\01_versionado_modelo\versionar_modelo.py
```

El artefacto se guarda en `data/05_mlops/model_registry/` y conserva el conjunto de prueba temporal sin usarlo para el ajuste final.
