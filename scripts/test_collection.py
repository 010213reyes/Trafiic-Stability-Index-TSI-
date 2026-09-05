#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba: Verificar que la recolección funciona localmente antes de GitHub Actions

Uso:
  python scripts/test_collection.py              # Recolectar datos de hoy
  python scripts/test_collection.py 2026-09-05   # Recolectar datos de fecha específica
  python scripts/test_collection.py --test       # Modo test (no guarda archivos)
"""

import sys
import os
import argparse
from datetime import datetime, timedelta

# Importar el script de recolección
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect_traffic_data import (
    recolectar_datos_diarios,
    generar_datos_sintéticos_calibrados,
    logger
)

import pandas as pd

# ============================================================================
# PRUEBAS
# ============================================================================

def prueba_generacion_sinteticos():
    """Prueba: Generar datos sintéticos sin guardar"""
    print("\n" + "="*70)
    print("PRUEBA 1: Generar datos sintéticos")
    print("="*70)
    
    try:
        fecha = datetime.now().date()
        df = generar_datos_sintéticos_calibrados(pd.Timestamp(fecha))
        
        print(f"✓ Generación exitosa")
        print(f"  Registros: {len(df)}")
        print(f"  Columnas: {list(df.columns)}")
        print(f"  Avenidas: {df['avenida'].nunique()}")
        print(f"  Velocidad rango: {df['velocidad_kmh'].min():.1f} - {df['velocidad_kmh'].max():.1f}")
        print(f"  Densidad rango: {df['densidad_veh_km'].min():.1f} - {df['densidad_veh_km'].max():.1f}")
        print(f"\n  Primeras 5 filas:")
        print(df.head(5).to_string())
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def prueba_recoleccion_completa(fecha_str=None):
    """Prueba: Recolección completa con archivo de salida"""
    print("\n" + "="*70)
    print("PRUEBA 2: Recolección completa (con archivo de salida)")
    print("="*70)
    
    try:
        if fecha_str:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        else:
            fecha = datetime.now().date()
        
        print(f"Recolectando datos para: {fecha}")
        archivo_csv, archivo_meta = recolectar_datos_diarios(fecha)
        
        # Verificar archivos
        if os.path.exists(archivo_csv) and os.path.exists(archivo_meta):
            df = pd.read_csv(archivo_csv)
            print(f"\n✓ Archivos generados exitosamente")
            print(f"  CSV: {archivo_csv}")
            print(f"  Size: {os.path.getsize(archivo_csv) / 1024:.1f} KB")
            print(f"  Metadata: {archivo_meta}")
            
            # Análisis básico
            print(f"\n  Análisis de datos:")
            print(f"  - Registros: {len(df)}")
            print(f"  - Avenidas: {df['avenida'].nunique()}")
            print(f"  - Periodo: {df['timestamp'].min()} a {df['timestamp'].max()}")
            
            # Estadísticas
            print(f"\n  Estadísticas de velocidad:")
            print(f"  - Media: {df['velocidad_kmh'].mean():.1f} km/h")
            print(f"  - Desv: {df['velocidad_kmh'].std():.1f} km/h")
            print(f"  - Min-Max: {df['velocidad_kmh'].min():.1f} - {df['velocidad_kmh'].max():.1f}")
            
            # Anomalías
            n_anomalias = (df['anomalia'] == 'sí').sum()
            print(f"\n  Eventos detectados: {n_anomalias} anomalías")
            
            return True
        else:
            print(f"✗ Archivos no generados")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def prueba_consolidacion():
    """Prueba: Verificar que se pueden cargar múltiples archivos"""
    print("\n" + "="*70)
    print("PRUEBA 3: Consolidación de múltiples días")
    print("="*70)
    
    try:
        DATA_DIR = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "02_recoleccion_automatica"
        )
        
        import glob
        csv_files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
        
        if not csv_files:
            print("ℹ No hay archivos para consolidar (primera ejecución)")
            return True
        
        print(f"Archivos encontrados: {len(csv_files)}")
        
        # Cargar y consolidar
        dfs = []
        for archivo in csv_files[-5:]:  # Últimos 5 días
            df = pd.read_csv(archivo)
            dfs.append(df)
            print(f"  - {os.path.basename(archivo)}: {len(df)} registros")
        
        if dfs:
            df_consolidado = pd.concat(dfs, ignore_index=True)
            print(f"\n✓ Consolidación exitosa")
            print(f"  Registros totales: {len(df_consolidado)}")
            print(f"  Cobertura: {(df_consolidado['timestamp'].max() - df_consolidado['timestamp'].min()).days} días")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def prueba_dependencias():
    """Prueba: Verificar que las dependencias están disponibles"""
    print("\n" + "="*70)
    print("PRUEBA 0: Verificar dependencias")
    print("="*70)
    
    requerimientos = ['pandas', 'numpy']
    todos_ok = True
    
    for modulo in requerimientos:
        try:
            __import__(modulo)
            print(f"✓ {modulo}")
        except ImportError:
            print(f"✗ {modulo} NO INSTALADO")
            print(f"  Instalar con: pip install {modulo}")
            todos_ok = False
    
    return todos_ok


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pruebas de recolección de datos de tráfico"
    )
    parser.add_argument(
        'fecha',
        nargs='?',
        default=None,
        help='Fecha en formato YYYY-MM-DD (opcional, default: hoy)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Modo test (solo genera, no guarda)'
    )
    parser.add_argument(
        '--rápido',
        action='store_true',
        help='Solo pruebas rápidas (sin archivo)'
    )
    
    args = parser.parse_args()
    
    print("\n" + "█"*70)
    print("█ PRUEBAS DE RECOLECCIÓN DE DATOS DE TRÁFICO")
    print("█"*70)
    
    # Prueba 0: Dependencias
    if not prueba_dependencias():
        print("\n✗ Instala dependencias y vuelve a intentar:")
        print("  pip install pandas numpy")
        sys.exit(1)
    
    # Prueba 1: Rápida (generación)
    if not prueba_generacion_sinteticos():
        sys.exit(1)
    
    # Prueba 2: Completa (si no es --rápido)
    if not args.rápido:
        if not prueba_recoleccion_completa(args.fecha):
            sys.exit(1)
        
        # Prueba 3: Consolidación
        if not prueba_consolidacion():
            sys.exit(1)
    
    # Resumen
    print("\n" + "█"*70)
    print("█ TODAS LAS PRUEBAS PASARON ✓")
    print("█"*70)
    print("\nPróximos pasos:")
    print("1. Hacer commit: git add . && git commit -m 'Automatización recolección'")
    print("2. Push a GitHub: git push origin main")
    print("3. Verificar Actions en GitHub (debería ejecutarse automáticamente)")
    print("4. Después de 30 días, consolidar datos en análisis/modelado")
    print()
    
    sys.exit(0)
