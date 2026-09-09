# Series históricas externas

Archivos públicos de tráfico utilizados para aprender patrones generales antes de calibrar y validar con Guadalajara.

| Archivo | Fuente | Cobertura | Resolución | Estructura validada |
|---|---|---|---|---|
| `METR-LA.csv` | [Zenodo 5724362](https://zenodo.org/records/5724362) | 207 sensores; 2012-03-01 a 2012-06-27 | 5 minutos | 34,272 timestamps y 207 columnas de sensores |
| `PEMS-BAY.csv` | [Zenodo 5724362](https://zenodo.org/records/5724362) | 325 sensores; 2017-01-01 a 2017-06-30 | 5 minutos | 52,116 timestamps y 325 columnas de sensores |

Los archivos se conservan sin modificar en `data/00_raw/`. La primera columna contiene el timestamp y las columnas restantes representan sensores. La normalización se realizará posteriormente en `data/01_processed/`.

## Procedencia

- Registro: `https://zenodo.org/records/5724362`
- Repositorio metodológico: `https://github.com/liyaguang/DCRNN`
- Descarga realizada: 2026-09-09
- Uso dentro del proyecto: datos reales externos para preentrenamiento y análisis de transferencia; no representan observaciones de Guadalajara.