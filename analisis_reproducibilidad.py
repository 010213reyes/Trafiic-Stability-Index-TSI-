#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Análisis de reproducibilidad: ¿Podemos validar nuestras definiciones en los datos existentes?
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("ANÁLISIS DE REPRODUCIBILIDAD: ¿Podemos observar congestión en datos reales?")
print("="*80)

# ============================================================================
# 1. DATOS SINTÉTICOS (Lo que SÍ podemos usar para validar)
# ============================================================================
print("\n1. SYNTHETIC_TRAFFIC.CSV - Variables para validar definiciones")
print("-" * 80)

df_synth = pd.read_csv('data/00_raw/synthetic_traffic.csv')
df_synth['timestamp'] = pd.to_datetime(df_synth['timestamp'])

print(f"Total de registros: {len(df_synth)}")
print(f"Avenidas únicas: {df_synth['road'].nunique()}")
print(f"Rango temporal: {df_synth['timestamp'].min()} a {df_synth['timestamp'].max()}")
print(f"Cobertura: {(df_synth['timestamp'].max() - df_synth['timestamp'].min()).days} días")
print(f"Resolución: cada 10 minutos")
print(f"\nVariables disponibles:")
print(f"  - velocity_kmh: velocidad ({df_synth['velocity_kmh'].min():.1f}-{df_synth['velocity_kmh'].max():.1f})")
print(f"  - density_veh_km: densidad ({df_synth['density_veh_km'].min():.1f}-{df_synth['density_veh_km'].max():.1f})")
print(f"  - flow_veh_h: flujo ({df_synth['flow_veh_h'].min():.0f}-{df_synth['flow_veh_h'].max():.0f})")
print(f"  - wait_time_sec: espera ({df_synth['wait_time_sec'].min():.1f}-{df_synth['wait_time_sec'].max():.1f} seg)")
print(f"  - stops_count: detenciones ({df_synth['stops_count'].min():.0f}-{df_synth['stops_count'].max():.0f})")

# ============================================================================
# 2. ¿PODEMOS OBSERVAR CONGESTIÓN?
# ============================================================================
print("\n\n2. ¿PODEMOS OBSERVAR CONGESTIÓN (baja velocidad + alta densidad)?")
print("-" * 80)

for road in df_synth['road'].unique()[:2]:  # Primeras 2 avenidas
    road_data = df_synth[df_synth['road'] == road].sort_values('timestamp')
    
    vel_mean = road_data['velocity_kmh'].mean()
    vel_q1 = road_data['velocity_kmh'].quantile(0.25)
    dens_q75 = road_data['density_veh_km'].quantile(0.75)
    
    # Definición de congestión: velocidad en cuartil bajo + densidad en cuartil alto
    congestion = road_data[
        (road_data['velocity_kmh'] <= vel_q1) & 
        (road_data['density_veh_km'] >= dens_q75)
    ]
    
    print(f"\n{road}:")
    print(f"  Velocidad media: {vel_mean:.2f} km/h (cuartil 1: {vel_q1:.2f})")
    print(f"  Densidad cuartil 75: {dens_q75:.2f} veh/km")
    print(f"  ✓ Eventos de congestión: {len(congestion)} / {len(road_data)} ({100*len(congestion)/len(road_data):.1f}%)")
    
    if len(congestion) > 0:
        print(f"    Primer evento: {congestion.iloc[0]['timestamp']}")
        print(f"    Velocidad en congestión: {congestion['velocity_kmh'].mean():.1f} km/h")

# ============================================================================
# 3. ¿PODEMOS OBSERVAR PRE-COLAPSO (deterioro progresivo)?
# ============================================================================
print("\n\n3. ¿PODEMOS OBSERVAR PRE-COLAPSO (deterioro gradual de velocidad)?")
print("-" * 80)

road_sample = df_synth['road'].unique()[0]
dates_unique = df_synth['timestamp'].dt.date.unique()

print(f"Muestra: {road_sample}")
print("Buscando días con mayor deterioro de velocidad...\n")

deterioration_scores = []
for date in dates_unique:
    day_data = df_synth[
        (df_synth['road'] == road_sample) & 
        (df_synth['timestamp'].dt.date == date)
    ].sort_values('timestamp')
    
    if len(day_data) > 5:
        velocities = day_data['velocity_kmh'].values
        # Score: diferencia máxima entre pico y valle (deterioro máximo)
        deterioration = velocities.max() - velocities.min()
        deterioration_scores.append((date, deterioration, day_data))

if deterioration_scores:
    deterioration_scores.sort(key=lambda x: x[1], reverse=True)
    date_worst, deterioration_worst, day_data_worst = deterioration_scores[0]
    
    print(f"Día con mayor deterioro: {date_worst} (deterioro: {deterioration_worst:.1f} km/h)")
    print("\nSecuencia de velocidades (cada 10 min):")
    print(f"{'Hora':<8} {'Velocidad':<12} {'Cambio':<10} {'Densidad':<10}")
    print("-" * 40)
    
    prev_vel = None
    for idx, row in day_data_worst.iterrows():
        hora = row['timestamp'].strftime('%H:%M')
        vel = row['velocity_kmh']
        dens = row['density_veh_km']
        
        if prev_vel is not None:
            delta = vel - prev_vel
            change = f"{delta:+.1f}" if abs(delta) > 0.5 else "→"
        else:
            change = "base"
        
        print(f"{hora:<8} {vel:>9.1f}    {change:>8} {dens:>9.2f}")
        prev_vel = vel

# ============================================================================
# 4. DATOS REALES - ¿Suficientes para validar?
# ============================================================================
print("\n\n4. DATOS REALES (traffic_data.csv + scraped_traffic.csv)")
print("-" * 80)

df_traffic = pd.read_csv('data/00_raw/traffic_data.csv')
df_scraped = pd.read_csv('data/00_raw/scraped_traffic.csv')

print(f"traffic_data.csv:")
print(f"  Registros: {len(df_traffic)}")
print(f"  Avenidas: {df_traffic['avenida'].nunique()}")
print(f"  Faltantes velocidad: {df_traffic['velocidad'].isna().sum()} ({100*df_traffic['velocidad'].isna().sum()/len(df_traffic):.1f}%)")
print(f"  Faltantes densidad: {df_traffic['densidad'].isna().sum()} ({100*df_traffic['densidad'].isna().sum()/len(df_traffic):.1f}%)")
print(f"  ✗ PROBLEMA: muy pocas observaciones para ver patrones")

print(f"\nscraped_traffic.csv:")
print(f"  Registros: {len(df_scraped)}")
print(f"  Avenidas: {df_scraped['avenida'].nunique()}")
print(f"  Faltantes velocidad: {df_scraped['velocidad'].isna().sum()}")
print(f"  ✗ PROBLEMA: datos muy limitados")

# ============================================================================
# 5. CONCLUSIÓN
# ============================================================================
print("\n\n" + "="*80)
print("CONCLUSIÓN: REPRODUCIBILIDAD Y NECESIDADES REALES")
print("="*80)
print(f"""
✓ PODEMOS USAR (ahora): synthetic_traffic.csv
  - Variables completas: velocidad, densidad, flujo, espera, detenciones
  - Observaciones: 5,040 (suficiente para ver patrones)
  - Resolución: 10 minutos (adecuada)
  - Avenidas múltiples: sí
  - Permiso para validar definiciones: SÍ

✗ NO PODEMOS USAR (todavía): traffic_data.csv, scraped_traffic.csv
  - Observaciones insuficientes (310 y 117)
  - Muchos faltantes (velocidad, densidad, ubicación)
  - No permite observar pre-colapso
  - Resolución temporal inconsistente

---
DECISIÓN CRÍTICA para el proyecto:
---

ESCENARIO A (Continuar con lo que tienes):
  1. Validar definiciones en synthetic_traffic.csv
  2. Crear "eventos etiquetados" manualmente en datos sintéticos
  3. Riesgo: el modelo aprendería en DATOS FABRICADOS
  4. Resultado: prototipo que no funcionará en realidad

ESCENARIO B (Obtener datos reales primero):
  1. Recolectar ≥30 días de datos REALES con:
     - Resolución: 5-15 minutos
     - Variables: velocidad, densidad, flujo, espera, detenciones
     - Múltiples avenidas
  2. Validar definiciones en datos reales
  3. Crear etiquetas VERDADERAS de congestión/pre-colapso
  4. Resultado: modelo que FUNCIONA en producción

RECOMENDACIÓN: Completar minería (documentar fuentes de definiciones),
pero después de eso, es URGENTE conseguir datos reales antes de ML.
""")
