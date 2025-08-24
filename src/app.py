# src/app.py
import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do .env
load_dotenv()

# Função para conectar ao banco PostgreSQL
def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

# Função para carregar dados de uma view
def carregar_view(nome_view):
    conn = conectar()
    df = pd.read_sql(f"SELECT * FROM {nome_view};", conn)
    conn.close()
    return df

# Configuração da interface do Streamlit
st.set_page_config(page_title="Dashboard IoT", layout="wide")
st.title("📊 Dashboard de Temperaturas IoT")

# 1. Banco completo: temperaturas por modelo
st.header("📋 Temperaturas por Modelo")
df_temp = carregar_view("vw_temperaturas_por_modelo")
st.dataframe(df_temp, use_container_width=True)

# 2. Média: mostra 'Média de temperaturas' + valor
st.header("📉 Média Geral das Temperaturas")
df_media = carregar_view("vw_media_temperatura_por_modelo")
st.dataframe(df_media, use_container_width=True)

# 3. Mínima: mostra id + valor mínimo
st.header("❄️ Temperatura Mínima Registrada")
df_min = carregar_view("vw_min_temp_por_modelo")
st.dataframe(df_min, use_container_width=True)

# 4. Máxima: mostra id + valor máximo
st.header("🔥 Temperatura Máxima Registrada")
df_max = carregar_view("vw_max_temp_por_modelo")
st.dataframe(df_max, use_container_width=True)
