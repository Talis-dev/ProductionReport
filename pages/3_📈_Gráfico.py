import streamlit as st
import time
import pandas as pd
import sqlite3
from config import DB_PATH

st.set_page_config(
    page_title="Gáfico",
    page_icon="📈",
)
st.markdown("# Gerar Gráfico")
st.sidebar.header("Tipo de Gráfico")
st.sidebar.selectbox("",["Peso Total","Estação de Queda","Classificação"])

st.sidebar.header("PERÍODO")
st.sidebar.date_input('DE',format="DD/MM/YYYY")
st.sidebar.date_input('ATE',format="DD/MM/YYYY")
st.sidebar.button("Carregar")