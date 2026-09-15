# Testing del proyecto TSI

## Propósito

Esta carpeta contiene el entorno aislado para probar el sistema de inteligencia artificial TSI. No reemplaza la aplicación principal ni modifica el pipeline de producción local.

## Ruta de pruebas aprobada

```text
Testing TSI
│
├── 0. Diseño del plan de pruebas
├── 1. Preparación del entorno de pruebas
├── 2. Pruebas de datos y pipeline
├── 3. Pruebas estadísticas
├── 4. Pruebas de algoritmos y modelos
├── 5. Pruebas de integración con SQL
├── 6. Interfaz de pruebas en Streamlit
├── 7. Pruebas de extremo a extremo
├── 8. Pruebas de reproducibilidad
├── 9. Pruebas de despliegue
└── 10. Manual y reporte final
```

## Alcance

- Validar datos, pipeline, modelos, TSI y reproducibilidad.
- Probar la interacción de una interfaz Streamlit con los componentes del proyecto.
- Registrar resultados, evidencias e incidencias.


## Estructura inicial

```text
testing/
├── README.md
└── streamlit/
    └── app_testing.py
```

## Interfaz de pruebas

`streamlit/app_testing.py` es el punto de entrada visual del entorno de testing. En esta primera etapa solo contiene la base de la interfaz. La conexión con el backend, los casos de prueba, el login simulado y los reportes se incorporarán en pasos posteriores.

## Regla de separación

Las pruebas reutilizarán la lógica real del proyecto cuando se conecte el backend. No se duplicará la lógica de procesamiento, estadística o modelos dentro de la interfaz.
