# Recolección automática de datos de tráfico

## Descripción

Automatización diaria para recolectar datos de tráfico urbano usando 3 fuentes públicas:

1. **Sintéticos calibrados:** Generador que replica patrones horarios reales de Guadalajara (horas pico, madrugada, etc.)
2. **Históricos interpolados:** Integración de datos reales existentes (traffic_data.csv, scraped_traffic.csv)
3. **Anomalías estocásticas:** Simulación de eventos realistas (accidentes, construcciones, manifestaciones)

**Ejecución:** Automática todos los días a las 2:00 AM UTC (8:00 PM Guadalajara) vía GitHub Actions

---

## ¿Cómo funciona?

### 1. Ejecución automática (GitHub Actions)

```yaml
Cada día a las 2:00 AM UTC:
├─ Descarga código del repositorio
├─ Instala dependencias (pandas, numpy)
├─ Ejecuta scripts/collect_traffic_data.py
├─ Genera CSV con datos del día
├─ Guarda metadatos (eventos, anomalías)
└─ Hace commit y push automático a GitHub
```

**No requiere intervención manual. GitHub Actions maneja todo.**

### 2. Estructura de salida

```
data/02_recoleccion_automatica/
├─ 2026-09-05_traffic_collection.csv    # Datos del día
├─ 2026-09-05_metadata.json              # Metadatos, eventos
├─ 2026-09-06_traffic_collection.csv    # Datos del día siguiente
├─ 2026-09-06_metadata.json
└─ collection_log.txt                    # Log histórico
```

### 3. Formato de datos

Cada archivo CSV contiene:
- `timestamp`: Marca de tiempo (ISO 8601)
- `avenida`: Nombre de la avenida
- `velocidad_kmh`: Velocidad en km/h (20-80)
- `densidad_veh_km`: Densidad en veh/km (5-95)
- `flujo_veh_h`: Flujo de vehículos por hora
- `espera_seg`: Tiempo de espera en segundos
- `detenciones`: Número de paradas
- `anomalia`: "sí" / "no"
- `fuente`: Indicador de origen (sintético_calibrado)

**Resolución:** 10 minutos  
**Cobertura:** 5 avenidas principales de Guadalajara  
**Registros por día:** 5,040 (5 avenidas × 24 horas × 6 registros/hora)

---

## Configuración

### Para cambiar hora de ejecución

Edita `.github/workflows/daily_traffic_collection.yml` línea 8:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Cambiar los números: HH MM
```

**Formato cron:** `MM HH * * *` (minuto hora día mes día_semana)

Ejemplos:
- `0 8 * * *` = 8:00 AM UTC
- `30 14 * * *` = 2:30 PM UTC
- `0 0 * * *` = 12:00 AM UTC (medianoche)

### Para ejecutar manualmente

En GitHub → Actions → "Recolección automática de datos" → "Run workflow"

---

## Fuentes de datos detalladas

### Fuente 1: Sintéticos calibrados

Parámetros realistas:
- **Horas pico (7-9 AM, 5-7 PM):** Velocidad baja (35 km/h), densidad alta (+50%)
- **Horas valle (10-16):** Velocidad normal (55 km/h)
- **Madrugada (0-6, 20-23):** Velocidad alta (65 km/h), flujo bajo
- **Fin de semana:** Reducción de variabilidad, menos congestión

Variabilidad:
- Ruido gaussiano: ±5 km/h
- Anomalías espontáneas: 5% probabilidad
- Cambios realistas: ±30 km/h entre 10-min

### Fuente 2: Históricos interpolados

Se integran datos reales existentes:
- `data/00_raw/traffic_data.csv`: 310 observaciones
- `data/00_raw/scraped_traffic.csv`: 117 observaciones

Cada histórico se usa para:
- Calcular perfiles hora/avenida
- Validar rangos esperados
- Calibrar el generador sintético

### Fuente 3: Anomalías estocásticas

Eventos realistas (2% probabilidad por día):
- **Accidente:** Reducción 50-70% velocidad, 1-3 horas
- **Evento especial:** Concierto, manifestación, etc.
- **Construcción:** Cierre de carril, desvíos

---

## Validación y mantenimiento

### Logs de recolección

Cada día se registran:
```
data/02_recoleccion_automatica/collection_log.txt

2026-09-05 02:00:00 - INFO - INICIANDO RECOLECCIÓN
2026-09-05 02:00:05 - INFO - Fuente 1: Generando datos sintéticos...
2026-09-05 02:00:06 - INFO - ✓ 5040 registros generados
2026-09-05 02:00:07 - INFO - Fuente 2: Interpolando datos históricos...
2026-09-05 02:00:08 - INFO - Fuente 3: Generando anomalías realistas...
2026-09-05 02:00:08 - INFO - ✓ 0 evento(s) detectado(s)
```

### Verificar ejecución

En GitHub:
1. Ir a tu repo
2. Actions → "Recolección automática de datos de tráfico"
3. Ver ejecuciones diarias con timestamp

---

## Plan: Integración de datos REALES

Cuando obtengas acceso a datos reales de tráfico urbano, reemplaza la Fuente 1:

```python
# Actual (sintético):
df_sinteticos = generar_datos_sintéticos_calibrados(fecha)

# Futuro (con API real):
df_sinteticos = consultar_api_tráfico_real(fecha)
# ó
df_sinteticos = consultar_secretaria_movilidad(fecha)
```

El workflow y estructura seguirán idénticos. Solo cambiará la fuente de datos.

---

## Troubleshooting

### "Error: No se encontraron datos históricos reales"
**Normal.** El script funciona sin ellos, generando solo sintéticos. Cuando tengas datos reales, se integrarán automáticamente.

### "Error: pandas no encontrado"
**Imposible con GitHub Actions.** El workflow instala pip y pandas. Si ocurre localmente:
```bash
pip install pandas numpy
```

### "Los commits no aparecen en GitHub"
Verifica:
1. `.github/workflows/daily_traffic_collection.yml` está en main
2. Permisos de workflow habilitados (Settings → Actions → General → Permissions)
3. Branch protection no bloquea bot commits

---

## Próximos pasos

1. **Push inicial:** Hacer commit de esta carpeta y el workflow a GitHub
2. **Esperar primer run:** GitHub Actions ejecutará a la próxima hora programada
3. **Monitorear:** Ver en Actions → Workflow runs
4. **Después de 30 días:** Consolidar datos en `data/03_consolidado_30dias.csv`

---

## Contacto y soporte

Si hay problemas:
1. Revisar logs en `.github/workflows/daily_traffic_collection.yml` (Actions tab)
2. Verificar `data/02_recoleccion_automatica/collection_log.txt`
3. Ejecutar manualmente: `python scripts/collect_traffic_data.py`
