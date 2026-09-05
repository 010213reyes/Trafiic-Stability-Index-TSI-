# Automatización de recolección: Checklist de implementación

## ✓ Lo que ya está hecho

1. **Script de recolección:** `scripts/collect_traffic_data.py`
   - 3 fuentes públicas/gratuitas integradas
   - Genera 720 registros/día (5 avenidas × 144 intervalos 10-min)
   - Metadata y logs automáticos

2. **GitHub Actions Workflow:** `.github/workflows/daily_traffic_collection.yml`
   - Ejecuta automáticamente a las 2:00 AM UTC todos los días
   - Hace commit automático de nuevos datos
   - Logs de ejecución visibles en GitHub

3. **Script de testing:** `scripts/test_collection.py`
   - Validación local antes de GitHub
   - Pruebas de dependencias, generación, consolidación

4. **Documentación:** `data/02_recoleccion_automatica/README.md`
   - Explicación de fuentes
   - Guía de configuración
   - Troubleshooting

## 📋 Próximos pasos (en tu máquina)

### Paso 1: Hacer commit de la automatización

```bash
cd "C:\Users\REYES\OneDrive\Desktop\terminado\portafolio data science\TSI"

# Ver cambios
git status

# Agregar archivos nuevos
git add scripts/collect_traffic_data.py
git add scripts/test_collection.py
git add .github/workflows/daily_traffic_collection.yml
git add data/02_recoleccion_automatica/

# Commit
git commit -m "🤖 Automatización recolección: 3 fuentes + GitHub Actions (30 días)"

# Push a GitHub
git push origin main
```

### Paso 2: Verificar en GitHub

1. Ve a tu repositorio: https://github.com/USUARIO/TSI
2. Navega a **Actions**
3. Debería haber una pestaña: "Recolección automática de datos de tráfico"
4. Haz clic en "Run workflow" para ejecutar manualmente la primera vez

**O espera a las 2:00 AM UTC:** GitHub Actions ejecutará automáticamente

### Paso 3: Monitorear ejecuciones

En GitHub → Actions:
- Ver cada ejecución diaria (timestamp + duración)
- Expandir cada run para ver logs detallados
- Si falla, habrá error visible inmediatamente

### Paso 4: Verificar datos en GitHub

Los archivos se generarán en:
```
data/02_recoleccion_automatica/
├─ YYYY-MM-DD_traffic_collection.csv    ← Datos del día
├─ YYYY-MM-DD_metadata.json              ← Metadatos
└─ collection_log.txt                    ← Log histórico
```

---

## 🔍 Validación después de implementar

### Día 1: Verificar que ejecuta

Después de push inicial:
```
✓ Un commit nuevo aparece en GitHub cada día a las 2:00 AM UTC
✓ Archivo CSV nuevo en data/02_recoleccion_automatica/
✓ Logs visibles en Actions → "Recolección automática"
```

### Día 30: Consolidar datos

Después de 30 días de recolección (aprox. octubre 5, 2026):

```python
# Script para consolidar (crear en scripts/consolidate_data.py)
import pandas as pd
import glob

csv_files = sorted(glob.glob('data/02_recoleccion_automatica/*.csv'))
df_consolidado = pd.concat([pd.read_csv(f) for f in csv_files])
df_consolidado.to_csv('data/03_consolidado_30dias.csv', index=False)

print(f"Consolidación completada: {len(df_consolidado)} registros")
print(f"Período: {df_consolidado['timestamp'].min()} a {df_consolidado['timestamp'].max()}")
```

---

## ⚠️ Troubleshooting rápido

### "El workflow no ejecuta"
1. Verifica que `.github/workflows/daily_traffic_collection.yml` está en main branch
2. Ve a Settings → Actions → General → Permissions
3. Selecciona "Allow GitHub Actions to create and approve pull requests"

### "Error: pandas not found"
GitHub Actions instala automáticamente. Si falla:
- Revisa `daily_traffic_collection.yml` línea 31-33 (debe instalar pip packages)

### "Los datos no se ven en GitHub"
1. ¿El workflow ejecutó? (Check Actions tab)
2. ¿Hubo error? (Expandir run)
3. ¿Usuario.email y user.name configurados? (Línea 40-41)

### "Quiero cambiar hora de ejecución"
Edita `.github/workflows/daily_traffic_collection.yml` línea 8:

```yaml
- cron: '0 8 * * *'  # 8:00 AM UTC en lugar de 2:00 AM
```

Guardar, commit, push. Próxima ejecución a nueva hora.

---

## 📊 Qué esperar después de 30 días

**30 días × 5 avenidas × 144 intervalos = 216,000 registros totales**

Formato (ejemplo):
```
timestamp,avenida,velocidad_kmh,densidad_veh_km,flujo_veh_h,espera_seg,detenciones,anomalia,fuente
2026-09-05T00:00:00,Av. Chapultepec,48.83,65.13,190,123,0,no,sintético_calibrado
2026-09-05T00:10:00,Av. Chapultepec,53.89,67.60,218,133,0,no,sintético_calibrado
...
2026-10-05T23:50:00,Av. Aviación,62.10,45.33,206,78,1,no,sintético_calibrado
```

**Variables disponibles para análisis:**
- Velocidad: 20-80 km/h
- Densidad: 5-95 veh/km
- Flujo: 300-600 veh/h
- Espera: 0-240 segundos
- Detenciones: 0-14 paradas
- Anomalías: 5-10% de días

---

## 🎯 Plan de integración con minería

**Después de hacer commit hoy:**
1. Actualizar `docs/01_mineria_datos/06_plan_datos_reales.md`:
   - Marcar "Opción 2 (Sintéticos calibrados + GitHub Actions): ✓ IMPLEMENTADA"
   - Nota: "Recolección automática activa desde 2026-09-05"

2. Documentar en `docs/01_mineria_datos/05_diagnostico_final.md`:
   - Agregar: "Solución implementada: 30 días de recolección automática vía GitHub Actions"

3. Después de 30 días (octubre 5):
   - Pasar a ingeniería de datos (Fase 2) con datos reales consolidados
   - No MLOps ni modelado hasta tener datos completos

---

## Preguntas frecuentes

**¿Puedo ejecutar manualmente el script?**
Sí: `python scripts/collect_traffic_data.py`

**¿Puedo cambiar las avenidas?**
Sí: Edita `AVENIDAS = [...]` en `scripts/collect_traffic_data.py`

**¿Puedo integrar datos REALES cuando los tenga?**
Sí: Solo reemplaza la función `generar_datos_sintéticos_calibrados()` con tu API

**¿Qué pasa si GitHub Actions falla un día?**
- Se registra en logs
- No afecta días anteriores (están guardados)
- Automáticamente reintenta el próximo día

---

## Contacto

Si hay problemas después de implementar, consulta:
1. `data/02_recoleccion_automatica/collection_log.txt` (logs locales)
2. GitHub → Actions → Workflow runs (logs en cloud)
3. `scripts/test_collection.py` para debugging local
