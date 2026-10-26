# 03 Monitoreo

Controla la calidad de los datos recibidos, los cambios de distribución, la cobertura de variables, las tasas de anomalías y el desempeño cuando existan etiquetas observadas.

## Entregables

- controles de calidad de entrada;
- reporte de drift descriptivo;
- seguimiento de tasas de anomalía y valores faltantes;
- criterios de alerta y límites de interpretación.

## Ejecución

Desde la raíz del proyecto:

```powershell
.venv\Scripts\python.exe docs\05_mlops\03_monitoreo\monitorear_flujo.py
```

El reporte se guarda en `data/05_mlops/monitoring/reporte_monitoreo.json`. Las alertas son controles operativos de esta demostración local, no sustituyen un sistema de observabilidad productivo.
