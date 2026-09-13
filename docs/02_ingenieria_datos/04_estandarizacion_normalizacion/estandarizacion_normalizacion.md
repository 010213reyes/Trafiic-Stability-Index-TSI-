# 2.4 Estandarización y normalización

## Estado

Completado.

## Actividades

- Unificar nombres de columnas.
- Normalizar tipos de datos y fechas.
- Convertir unidades documentadas.
- Estandarizar identificadores, ciudades y fuentes.
- Convertir fuentes anchas a formato largo cuando corresponda.

## Implementación

El script se ejecuta con:

```text
python docs/02_ingenieria_datos/04_estandarizacion_normalizacion/estandarizar_fuentes.py
```

Las salidas se generan en:

```text
data/01_processed/normalized/
```

Cada salida contiene el contrato común. Las variables no disponibles permanecen nulas. Los valores de METR-LA y PEMS-BAY se conservan en `valor_fuente` hasta confirmar su unidad; no se presentan todavía como `velocidad_kmh`.

El manifiesto de la ejecución se genera en:

```text
data/01_processed/normalized/normalization_manifest.json
```

## Entregable

Datos procesados con el contrato común y procedencia conservada por fuente.
