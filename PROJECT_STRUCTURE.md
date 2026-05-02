# Estructura Organizacional del Proyecto TSI

## 📁 Estructura General

```
TSI/
├── notebooks/                    # Todos los notebooks organizados
│   ├── 01_Data_Collection/      # Recopilación de datos
│   │   ├── 01_Synthetic_Traffic_Data.ipynb
│   │   ├── 02_Historical_Data_Import.ipynb
│   │   ├── 03_Crowdsourcing_Collection.ipynb
│   │   ├── Realistic_Traffic_Modeling.ipynb
│   │   └── Scraping_Traffic.ipynb
│   │
│   └── 02_Data_Processing/      # Procesamiento y limpieza de datos
│       ├── 01_Data_Quality_Assessment.ipynb    # Diagnóstico
│       ├── 02_Data_Cleaning.ipynb              # Limpieza
│       ├── 03_Data_Validation.ipynb            # Validación
│       ├── 04_Exploratory_Data_Analysis.ipynb  # Análisis
│       └── Data_Ingestion_Basic_Procesing.ipynb
│
├── data/                         # Datos organizados por etapa
│   ├── 00_raw/                  # Datos crudos sin procesar
│   │   ├── traffic_data.csv
│   │   ├── scraped_traffic.csv
│   │   ├── synthetic_traffic.csv
│   │   ├── crowdsourcing_raw.csv
│   │   └── crowdsourcing_aggregated.csv
│   │
│   ├── 01_processed/            # Datos procesados (transformaciones)
│   │   ├── traffic_data_transformed.csv
│   │   └── [características derivadas]
│   │
│   ├── 02_clean/                # Datos limpios validados
│   │   ├── traffic_data_clean.csv
│   │   ├── traffic_data_with_classifications.csv
│   │   ├── estadisticas_por_avenida.csv
│   │   └── [visualizaciones EDA]
│   │
│   └── 03_algorithm_output/     # Salida del algoritmo/modelo
│       ├── tsi_predictions.csv
│       ├── risk_analysis.csv
│       └── [resultados finales]
│
├── README.md                     # Documentación del proyecto
├── PROJECT_STRUCTURE.md          # Este archivo
└── [otros archivos]

```

## 🗂️ Descripción de Carpetas

### **notebooks/**

#### **01_Data_Collection/** - Recopilación de Datos
**Objetivo**: Obtener datos de diferentes fuentes

Notebooks:
- `Scraping_Traffic.ipynb` - Web scraping de sitios de tráfico
- `01_Synthetic_Traffic_Data.ipynb` - Generación de datos sintéticos
- `02_Historical_Data_Import.ipynb` - Importación de datos históricos
- `03_Crowdsourcing_Collection.ipynb` - Datos de crowdsourcing
- `Realistic_Traffic_Modeling.ipynb` - Modelado realista

**Salida**: Archivos CSV en `data/00_raw/`

#### **02_Data_Processing/** - Procesamiento y Limpieza
**Objetivo**: Garantizar calidad y transformar datos

Notebooks (ejecución secuencial):

1. **01_Data_Quality_Assessment.ipynb** - Diagnóstico
   - Detecta valores nulos, tipos incorrectos, rangos inválidos
   - Identifica duplicados y outliers
   - **Salida**: Reporte de problemas

2. **02_Data_Cleaning.ipynb** - Limpieza Activa
   - Convierte tipos de datos
   - Imputa valores nulos
   - Elimina duplicados
   - Trata outliers
   - **Salida**: `data/02_clean/traffic_data_clean.csv`

3. **03_Data_Validation.ipynb** - Validación
   - Verifica integridad post-limpieza
   - Confirma completitud (0% nulos)
   - Valida rangos y consistencia
   - **Salida**: Dataset validado

4. **04_Exploratory_Data_Analysis.ipynb** - Análisis Exploratorio (EDA)
   - Estadísticas descriptivas
   - Correlaciones entre variables
   - Identificación de avenidas críticas
   - Detección de patrones
   - Clasificación de estados
   - **Salida**: Gráficos PNG + insights

### **data/**

#### **00_raw/** - Datos Crudos
- **Contenido**: Datos originales sin procesar
- **Origen**: Directamente de fuentes (scraping, APIs, importación)
- **Características**: Pueden contener errores, valores nulos, duplicados
- **No modificar**: Estos son los datos originales

#### **01_processed/** - Datos Procesados
- **Contenido**: Datos después de transformaciones
- **Operaciones**: Feature engineering, cálculos derivados
- **Uso**: Intermediario en el pipeline
- **Nota**: Para futuro uso en algoritmo

#### **02_clean/** - Datos Limpios y Validados
- **Contenido**: Datos listos para análisis
- **Garantías**: 0% valores nulos, sin duplicados, rangos válidos
- **Características**:
  - `traffic_data_clean.csv` - Dataset limpio principal
  - `traffic_data_with_classifications.csv` - Con estados clasificados
  - `estadisticas_por_avenida.csv` - Resumen estadístico
  - Visualizaciones PNG del EDA

#### **03_algorithm_output/** - Salida del Algoritmo
- **Contenido**: Resultados del modelo/algoritmo TSI
- **Ejemplos**:
  - Predicciones de pre-colapso
  - Análisis de riesgo
  - Métricas TSI calculadas
  - Validación de modelo

## 🔄 Flujo de Datos

```
Fuentes de datos (Web, API, Import)
         ↓
notebooks/01_Data_Collection/
         ↓
data/00_raw/ (Datos crudos)
         ↓
notebooks/02_Data_Processing/01 (Diagnóstico)
         ↓
notebooks/02_Data_Processing/02 (Limpieza)
         ↓
data/02_clean/ (Datos limpios)
         ↓
notebooks/02_Data_Processing/03 (Validación)
         ↓
notebooks/02_Data_Processing/04 (EDA)
         ↓
data/02_clean/[visualizaciones e insights]
         ↓
[Feature Engineering - Próximo]
         ↓
[Construcción de métrica TSI - Próximo]
         ↓
data/03_algorithm_output/ (Resultados finales)
```

## 📊 Gestión de Archivos

### ✅ Convenciones de Nombres

- **Notebooks**: `NN_Descripcion.ipynb` (ej: `01_Data_Quality_Assessment.ipynb`)
- **Datos**: `dataset_stage_version.csv` (ej: `traffic_data_clean.csv`)
- **Carpetas**: `NN_Stage_Name` (ej: `00_raw`, `01_processed`, `02_clean`)

### 🔐 Política de Datos

- **00_raw/**: Solo lectura - No modificar
- **01_processed/**: Datos intermedios - Puede eliminarse y regenerarse
- **02_clean/**: Datos validados - Referencia para análisis
- **03_algorithm_output/**: Resultados - Para entrega/reporte

## 🚀 Instrucciones de Uso

### Para agregar nuevos notebooks:

1. **Si es de recopilación**: Colocar en `notebooks/01_Data_Collection/`
2. **Si es de procesamiento**: Colocar en `notebooks/02_Data_Processing/`
3. Seguir convención de nombres: `NN_Descripcion_Corta.ipynb`
4. Actualizar esta documentación

### Para agregar nuevos datos:

1. **Si son crudos**: `data/00_raw/nombre_dataset.csv`
2. **Si son procesados**: `data/01_processed/` (después de transformaciones)
3. **Si están limpios**: `data/02_clean/` (después de validación)
4. **Si son resultados**: `data/03_algorithm_output/` (salida del modelo)

### Para mantener limpio:

```bash
# No debe comprometerse a git:
data/01_processed/  # (regenerable)
data/03_algorithm_output/  # (resultados temporales)

# Siempre debe estar en git:
notebooks/  # (código)
data/00_raw/  # (datos originales)
data/02_clean/  # (datos validados de referencia)
README.md
PROJECT_STRUCTURE.md
```

## 📝 Notas Importantes

1. **Reproducibilidad**: Los datos en `00_raw` son la fuente de verdad
2. **Versionamiento**: `02_clean` es el estado estable del dataset
3. **Debugging**: Si algo falla, verificar en orden:
   - ¿Existen los datos en `00_raw`?
   - ¿Se ejecutaron los notebooks en orden?
   - ¿Se actualizaron los paths después de mover archivos?

## 🔗 Relación entre Carpetas

```
Recolección → Crudos → Diagnóstico → Limpieza → Validación → Análisis → Insights
    ↓            ↓          ↓          ↓           ↓            ↓         ↓
 01_Data_       00_raw     01_QA      02_Clean    03_Validar  04_EDA   02_clean/
 Collection                                                             insights
```

---
**Última actualización**: 1 de mayo de 2026
**Versión**: 1.0 - Estructura base completada
