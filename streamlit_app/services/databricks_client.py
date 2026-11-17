import streamlit as st
from databricks import sql
import pandas as pd


def conectar_databricks():
    config = st.secrets["databricks"]

    return sql.connect(
        server_hostname=config["server_hostname"],
        http_path=config["http_path"],
        access_token=config["access_token"],
    )


def consultar_databricks(query):
    with conectar_databricks() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(query)
            columnas = [col[0] for col in cursor.description]
            filas = cursor.fetchall()

    return columnas, filas






@st.cache_data(ttl=600, show_spinner="Consultando Databricks...")
def obtener_predicciones_mlops():
    columnas, filas = consultar_databricks("""
        SELECT *
        FROM workspace.tsi.pems_bay_predicciones_v2
        ORDER BY timestamp DESC
        LIMIT 100
    """)

    return pd.DataFrame(
        [tuple(fila) for fila in filas],
        columns=columnas,
    )