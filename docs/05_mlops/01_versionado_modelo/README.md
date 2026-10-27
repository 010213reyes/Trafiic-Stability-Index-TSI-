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

El artefacto se guarda en `data/05_mlops/model_registry/` y conserva el conjunto de prueba temporal sin usarlo para el ajuste final. Si no se indica una versión, el script detecta la última versión de `rf_tsi_internacional` e incrementa automáticamente el parche: `v1.0.0` -> `v1.0.1`. También se puede fijar una versión manual con `--model-version`.

## Modelos comparativos

El ciclo también puede registrar los modelos evaluados que acompañan la selección:

```powershell
.venv\Scripts\python.exe docs\05_mlops\01_versionado_modelo\registrar_modelos_comparacion.py
```

Este script registra Ridge como modelo serializado y el baseline de persistencia como regla determinista. Random Forest permanece como modelo activo de inferencia; Ridge y baseline quedan disponibles para trazabilidad y comparación.
