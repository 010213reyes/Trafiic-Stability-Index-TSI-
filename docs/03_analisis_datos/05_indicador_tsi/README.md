# 05 Indicador TSI

Esta subfase prepara un componente TSI provisional y documenta lo que aun falta para definir el indicador final.

## Ejecucion provisional

```powershell
.\.venv\Scripts\python.exe scripts\analysis\05_indicador_tsi_provisional.py
```

El script genera `data/03_analysis_output/indicador_tsi/tsi_provisional_diario.csv` y `metodo.json`.

## Metodo actual

- Normalizacion min-max dentro de cada fuente y metrica.
- Escala provisional de 0 a 100.
- Mayor velocidad equivale provisionalmente a mayor estabilidad.
- Mayor congestion, intensidad o longitud congestionada equivale provisionalmente a menor estabilidad.
- Las fuentes no se mezclan en una media internacional.

## Resultado inicial

El calculo completo genero 9.757 combinaciones dia-fuente. Las medias provisionales fueron aproximadamente 54,16 para Istanbul, 76,74 para METR-LA, 98,61 para Madrid, 73,58 para PEMS-BAY y 94,24 para Sao Paulo.

Estas diferencias no representan aun que una ciudad sea mas estable que otra. El resultado es sensible a extremos, rangos de origen, ventanas temporales y unidades.

## Pendientes antes del indicador final

1. Verificar unidades y significado operacional de cada metrica.
2. Evaluar normalizacion robusta frente a min-max.
3. Definir una ventana temporal comun o comparar solo dentro de cada fuente.
4. Calibrar la interpretacion con Guadalajara.
5. Validar la formula y sus ponderaciones antes de publicarla como TSI final.
