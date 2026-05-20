import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title='TSI Dashboard', layout='wide')

project_root = next((candidate for candidate in [Path(__file__).resolve().parent, Path.cwd(), Path.cwd().parent, Path.cwd().parent.parent] if (candidate / 'data' / '02_clean').exists()), Path.cwd())
source_path = project_root / 'data' / '02_clean' / 'traffic_enriched.csv'
if_path = project_root / 'data' / '02_clean' / 'filtered_isolation_forest.csv'
lof_path = project_root / 'data' / '02_clean' / 'filtered_local_outlier_factor.csv'
dbscan_path = project_root / 'data' / '02_clean' / 'filtered_dbscan.csv'
comparison_path = project_root / 'notebooks' / '02_Data_Processing' / '08_Algorithm_Comparison_and_TSI.ipynb'

st.title('Traffic Stability Index')
st.caption('Panel ejecutivo para revisar la señal principal del proyecto TSI.')

st.info('Esta primera version del dashboard carga los artefactos ya validados por los notebooks y deja la base lista para ampliar visualizaciones.')

col1, col2, col3, col4 = st.columns(4)

for column, label, path in [
    (col1, 'Dataset base', source_path),
    (col2, 'Isolation Forest', if_path),
    (col3, 'Local Outlier Factor', lof_path),
    (col4, 'DBSCAN', dbscan_path),
]:
    with column:
        st.metric(label, 'Disponible' if path.exists() else 'Pendiente')

st.divider()

if source_path.exists():
    source_df = pd.read_csv(source_path)
    st.subheader('Resumen del dataset base')
    st.write(source_df.head())
else:
    st.warning('No se encontró traffic_enriched.csv en data/02_clean.')

st.subheader('Archivos clave del proyecto')
for file_path in [if_path, lof_path, dbscan_path]:
    st.write(f"- {file_path.name}: {'encontrado' if file_path.exists() else 'faltante'}")

st.subheader('Siguientes pantallas sugeridas')
st.write('- Comparación homogénea de algoritmos')
st.write('- Distribución del TSI propuesto')
st.write('- Conclusión ejecutiva y decisión final')
