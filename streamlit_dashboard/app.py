from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(page_title='TSI Dashboard', page_icon='TSI', layout='wide')


def resolve_project_root() -> Path:
    return next(
        (
            candidate
            for candidate in [Path(__file__).resolve().parent, Path.cwd(), Path.cwd().parent, Path.cwd().parent.parent]
            if (candidate / 'data' / '02_clean').exists()
        ),
        Path.cwd(),
    )


PROJECT_ROOT = resolve_project_root()
DATA_ROOT = PROJECT_ROOT / 'data'
CLEAN_ROOT = DATA_ROOT / '02_clean'
OUTPUT_ROOT = DATA_ROOT / '03_algorithm_output'

SOURCE_PATH = CLEAN_ROOT / 'traffic_enriched.csv'
IF_PATH = CLEAN_ROOT / 'filtered_isolation_forest.csv'
LOF_PATH = CLEAN_ROOT / 'filtered_local_outlier_factor.csv'
DBSCAN_PATH = CLEAN_ROOT / 'filtered_dbscan.csv'

IF_SUMMARY_PATH = OUTPUT_ROOT / 'local_outlier_factor_summary.csv'
LOF_SUMMARY_PATH = OUTPUT_ROOT / 'local_outlier_factor_summary.csv'
DBSCAN_SUMMARY_PATH = OUTPUT_ROOT / 'dbscan_summary.csv'

RANKING_IMAGE = OUTPUT_ROOT / '02_algorithm_ranking.png'
COMPARISON_IMAGE = OUTPUT_ROOT / '01_algorithm_comparison.png'
FILTER_IMPACT_IMAGE = OUTPUT_ROOT / '09_filtrado_impacto.png'
VARIABILITY_IMAGE = OUTPUT_ROOT / '10_variability_comparison.png'
IF_SUMMARY_IMAGE = OUTPUT_ROOT / '11_isolation_forest_summary.png'
IF_BOXPLOTS_IMAGE = OUTPUT_ROOT / '12_isolation_forest_boxplots.png'
LOF_PCA_IMAGE = OUTPUT_ROOT / 'local_outlier_factor_pca.png'
LOF_SCORES_IMAGE = OUTPUT_ROOT / 'local_outlier_factor_scores.png'
DBSCAN_PCA_IMAGE = OUTPUT_ROOT / 'dbscan_pca_clusters.png'
DBSCAN_KDIST_IMAGE = OUTPUT_ROOT / 'dbscan_kdistance_curve.png'
DBSCAN_CLUSTER_IMAGE = OUTPUT_ROOT / 'dbscan_cluster_sizes.png'


def load_csv(path: Path) -> pd.DataFrame | None:
    return pd.read_csv(path) if path.exists() else None


def load_metric(summary_df: pd.DataFrame, metric: str):
    if summary_df is None:
        return None
    matches = summary_df.loc[summary_df['metric'] == metric, 'value']
    if matches.empty:
        return None
    return matches.iloc[0]


source_df = load_csv(SOURCE_PATH)
if_df = load_csv(IF_PATH)
lof_df = load_csv(LOF_PATH)
dbscan_df = load_csv(DBSCAN_PATH)
lof_summary = load_csv(LOF_SUMMARY_PATH)
dbscan_summary = load_csv(DBSCAN_SUMMARY_PATH)

st.title('Traffic Stability Index')
st.caption('Panel ejecutivo para la narrativa final del proyecto TSI')

st.markdown(
    'Este dashboard muestra solo lo que cambia la lectura final del proyecto: la comparación entre algoritmos, la señal del TSI y las conclusiones que conectan el análisis de principio a fin.'
)

if source_df is None:
    st.error('No se encontró el dataset base traffic_enriched.csv en data/02_clean.')
    st.stop()

source_count = len(source_df)
dbscan_clusters = int(load_metric(dbscan_summary, 'clusters_detectados') or 0)
dbscan_noise_pct = float(load_metric(dbscan_summary, 'porcentaje_ruido') or 0)
dbscan_retention_pct = float(load_metric(dbscan_summary, 'porcentaje_retenido') or 0)

if_retention = round(len(if_df) / source_count * 100, 2) if if_df is not None else None
if_noise = round((source_count - len(if_df)) / source_count * 100, 2) if if_df is not None else None
lof_retention = float(load_metric(lof_summary, 'porcentaje_retenido') or 0)
lof_noise = float(load_metric(lof_summary, 'porcentaje_anomalia') or 0)

top_left, top_mid_left, top_mid_right, top_right = st.columns(4)
with top_left:
    st.metric('Registros base', f'{source_count:,}')
with top_mid_left:
    st.metric('DBSCAN retención', f'{dbscan_retention_pct:.2f}%')
with top_mid_right:
    st.metric('DBSCAN ruido', f'{dbscan_noise_pct:.2f}%')
with top_right:
    st.metric('Clusters DBSCAN', f'{dbscan_clusters}')

st.divider()

overview_tab, comparison_tab, tsi_tab, conclusion_tab = st.tabs([
    'Resumen ejecutivo',
    'Comparación de algoritmos',
    'TSI final',
    'Conclusión',
])

with overview_tab:
    left, right = st.columns([1.05, 0.95])
    with left:
        st.subheader('Lectura final del proyecto')
        st.markdown(
            '- **Isolation Forest** depura muy bien, pero su señal es principalmente binaria.\n'
            '- **LOF** captura vecindad local y da una depuración más suave.\n'
            '- **DBSCAN** separa regímenes densos y ofrece la mejor señal estructural para TSI.'
        )
        st.markdown(
            'La decisión final del proyecto se apoya en DBSCAN como validación estructural, mientras que los otros dos algoritmos quedan como filtros de apoyo.'
        )
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric('Isolation Forest', f'{if_retention:.2f}%' if if_retention is not None else 'N/D', f'ruido {if_noise:.2f}%' if if_noise is not None else None)
        with summary_cols[1]:
            st.metric('LOF', f'{lof_retention:.2f}%', f'anomalias {lof_noise:.2f}%')
        with summary_cols[2]:
            st.metric('DBSCAN', f'{dbscan_retention_pct:.2f}%', f'ruido {dbscan_noise_pct:.2f}%')
    with right:
        if RANKING_IMAGE.exists():
            st.image(str(RANKING_IMAGE), caption='Ranking comparativo de algoritmos', use_container_width=True)
        else:
            st.warning('No se encontró 02_algorithm_ranking.png.')

with comparison_tab:
    st.subheader('Comparación homogénea')
    rows = []
    if if_df is not None:
        rows.append({
            'Algoritmo': 'Isolation Forest',
            'Retención (%)': if_retention,
            'Ruido / outliers (%)': if_noise,
            'Estabilidad': 'Baja',
            'Regímenes detectados': 1,
        })
    if lof_df is not None:
        rows.append({
            'Algoritmo': 'Local Outlier Factor',
            'Retención (%)': lof_retention,
            'Ruido / outliers (%)': lof_noise,
            'Estabilidad': 'Media',
            'Regímenes detectados': 1,
        })
    if dbscan_df is not None:
        rows.append({
            'Algoritmo': 'DBSCAN',
            'Retención (%)': dbscan_retention_pct,
            'Ruido / outliers (%)': dbscan_noise_pct,
            'Estabilidad': 'Alta',
            'Regímenes detectados': dbscan_clusters,
        })

    comparison_df = pd.DataFrame(rows)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        if COMPARISON_IMAGE.exists():
            st.image(str(COMPARISON_IMAGE), caption='Comparación general de algoritmos', use_container_width=True)
        else:
            st.warning('No se encontró 01_algorithm_comparison.png.')
    with c2:
        if VARIABILITY_IMAGE.exists():
            st.image(str(VARIABILITY_IMAGE), caption='Comparación de variabilidad', use_container_width=True)
        else:
            st.warning('No se encontró 10_variability_comparison.png.')

with tsi_tab:
    st.subheader('TSI propuesto')
    source_df['TSI_propuesto'] = (
        0.45 * source_df['speed_congestion']
        + 0.35 * source_df['densidad_norm']
        + 0.20 * source_df['detenciones_norm']
    ).clip(0, 1)

    tsi_stats = source_df['TSI_propuesto'].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99])
    st.metric('Correlación con el TSI actual', f"{source_df['TSI'].corr(source_df['TSI_propuesto']):.4f}" if 'TSI' in source_df.columns else 'N/D')

    tsi_col1, tsi_col2 = st.columns([1, 1])
    with tsi_col1:
        st.markdown(
            'La fórmula final queda anclada en tres componentes:\n'
            '- congestión relativa\n'
            '- densidad normalizada\n'
            '- detenciones normalizadas'
        )
        st.code('TSI = 0.45 * speed_congestion + 0.35 * densidad_norm + 0.20 * detenciones_norm', language='text')
        st.write(tsi_stats.to_frame(name='TSI_propuesto'))
    with tsi_col2:
        if IF_SUMMARY_IMAGE.exists():
            st.image(str(IF_SUMMARY_IMAGE), caption='Resumen visual de Isolation Forest', use_container_width=True)
        elif IF_BOXPLOTS_IMAGE.exists():
            st.image(str(IF_BOXPLOTS_IMAGE), caption='Resumen visual de depuración', use_container_width=True)
        else:
            st.info('No se encontró una visualización de resumen para esta sección.')

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        if LOF_PCA_IMAGE.exists():
            st.image(str(LOF_PCA_IMAGE), caption='LOF: proyección PCA', use_container_width=True)
        else:
            st.warning('No se encontró local_outlier_factor_pca.png.')
    with bottom_right:
        if DBSCAN_PCA_IMAGE.exists():
            st.image(str(DBSCAN_PCA_IMAGE), caption='DBSCAN: proyección PCA de clusters', use_container_width=True)
        else:
            st.warning('No se encontró dbscan_pca_clusters.png.')

with conclusion_tab:
    st.subheader('Decisión final')
    st.success(
        'DBSCAN se mantiene como validación estructural principal porque conserva una retención razonable y separa regímenes densos con ruido moderado, lo que aporta la señal más útil para definir riesgo.'
    )
    st.markdown(
        'Isolation Forest queda como depuración fuerte y LOF como validación local. La narrativa final del proyecto se apoya en esta división de roles para pasar de filtrado a interpretación.'
    )

    if DBSCAN_KDIST_IMAGE.exists() and DBSCAN_CLUSTER_IMAGE.exists():
        c_left, c_right = st.columns(2)
        with c_left:
            st.image(str(DBSCAN_KDIST_IMAGE), caption='DBSCAN: curva k-distance', use_container_width=True)
        with c_right:
            st.image(str(DBSCAN_CLUSTER_IMAGE), caption='DBSCAN: tamaños de clusters', use_container_width=True)

    st.markdown('### Siguientes pasos')
    st.write('1. Ajustar el dashboard para navegación por páginas si quieres una versión más formal.')
    st.write('2. Exportar una versión ejecutiva con conclusiones y figuras clave.')
    st.write('3. Conectar este dashboard al README final del proyecto como la capa de presentación.')
