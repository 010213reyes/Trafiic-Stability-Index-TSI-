# 09 Formulacion del TSI

Esta subfase formaliza el TSI provisional calculado en `03_analisis_datos`.

## Formula

Para cada fuente y metrica se conserva una escala relativa de 0 a 100:

- si un valor alto representa estabilidad, se usa `(x - min) / (max - min) * 100`;
- si un valor bajo representa estabilidad, se usa `(max - x) / (max - min) * 100`.

Los limites se calculan dentro de la fuente y metrica. No se mezclan unidades ni se interpreta el resultado como comparacion objetiva entre ciudades.

## Notebook

`01_Formulacion_TSI_Internacional.ipynb`

El resultado se guarda en `data/04_model_output/tsi/formulacion_tsi_provisional.json`.
