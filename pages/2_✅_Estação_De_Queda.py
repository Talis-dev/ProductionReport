import streamlit as st
import time
import pandas as pd
import sqlite3
from config import DB_PATH

st.set_page_config(
    page_title="Estação de queda",
    page_icon="✅",
)
st.markdown("# Estação de queda")
st.sidebar.header("PERÍODO")
st.sidebar.date_input('DE',format="DD/MM/YYYY")
st.sidebar.date_input('ATE',format="DD/MM/YYYY")
st.sidebar.button("Carregar")