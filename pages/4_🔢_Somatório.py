import streamlit as st
import time
import pandas as pd
import sqlite3
import locale
from config import DB_PATH ,LOCALE

##locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

try:
    locale.setlocale(locale.LC_TIME, LOCALE)
except locale.Error:
    print(f"Localidade {LOCALE} não está disponível no sistema.")

st.set_page_config(
    page_title="Somatório",
    page_icon="🔢",
)
st.markdown("# Gerar Somatório")
st.sidebar.header("Tipo de Relatório")
type_soma = st.sidebar.selectbox("",["Soma Total e Média","Por Faixa","Por Drop"])

st.sidebar.header("PERÍODO")


data_inicial = st.sidebar.date_input('DE:',format="DD/MM/YYYY") 
if data_inicial:
    data_peak_de = data_inicial.strftime('%Y-%m-%d')


data_final = st.sidebar.date_input('ATE:',format="DD/MM/YYYY")
if data_final:
    data_peak_ate = data_final.strftime('%Y-%m-%d')


botao_precionado = st.sidebar.button(':blue[Carregar]')
################################################################################# 
if botao_precionado:
    if type_soma == "Soma Total e Média":
        dias = (data_final - data_inicial).days
        st.write(f'## Total e Média no Período de {dias} Dias')
        with st.spinner('Aguarde Carregando...'):
            time.sleep(2)
            try:
                conexao = sqlite3.connect(DB_PATH)  
                cursor = conexao.cursor()
                consulta_sql = f"""
                SELECT AVG(PESOLIQUIDO) as MEDIA_PESOLIQUIDO,
                SUM(PESOLIQUIDO) as TOTAL_PESOLIQUIDO,
                COUNT(*) as QUANTIDADE_ITENS
                FROM PESAGENS
                WHERE DATA BETWEEN ? AND ?
                AND PESOLIQUIDO > 0.9;
                """
                cursor.execute(consulta_sql, (data_peak_de, data_peak_ate))
                resultados = cursor.fetchone()
                
                if resultados and resultados[2] > 0:
                    print(f'MÉDIA PESOLIQUIDO: {resultados[0]}')
                    print(f'TOTAL PESOLIQUIDO: {resultados[1]}')
                    print(f'QUANTIDADE DE ITENS: {resultados[2]}')

                    media_arredondada = round(resultados[0], 3)

                    st.write('## QUANTIDADE DE AVES: ', resultados[2])
                    st.write('## SOMA PESO TOTAL:  Kg', resultados[1])
                    st.write('## MÉDIA CALCULADA:  Kg', media_arredondada)
                else:
                    st.write('## Nenhum dado encontrado para o período selecionado.')
            except sqlite3.Error as e:
                st.write(f'Erro ao acessar o banco de dados: {e}')
            finally:
                if conexao:
                    conexao.close()  # fecha a conexão com o banco de dados




##########################################################################################
if botao_precionado: 
    if type_soma == "Por Faixa": 
        st.write('## POR FAIXA DE PESO')
        st.write(f'### {data_inicial.strftime('%d de %B de %y')}  A  {data_final.strftime('%d de %B de %y')}')
        with st.spinner('Aguarde Carregando...'):
            time.sleep(2)
            try:
                conexao = sqlite3.connect(DB_PATH)  
                cursor = conexao.cursor()

                consulta_sql = f"""
                SELECT FAIXA, NOMEFAIXA,
                PESOMINIMO as PESO_MIN,
                PESOMAXIMO as PESO_MAX,
                AVG(PESOLIQUIDO) as MEDIA_PESO, 
                SUM(PESOLIQUIDO) as TOTAL_PESO
                FROM PESAGENS
                WHERE DATA BETWEEN ? AND ?
                AND PESOLIQUIDO > 0.9
                GROUP BY NOMEFAIXA;
                """
                cursor.execute(consulta_sql, (data_peak_de, data_peak_ate))
                resultados = cursor.fetchall()
                
                if resultados:
                    df = pd.DataFrame(resultados, columns=['FAIXA', 'NOME DA FAIXA', 'PESO MIN', 'PESO MAX', 'MÉDIA', 'PESO TOTAL'])
                    df['MÉDIA'] = df['MÉDIA'].round(3)  # arredonda somente a coluna média
                    st.dataframe(df)
                    ##print(df)
                else:
                    st.write('## Nenhum dado encontrado para o período selecionado.')
            except sqlite3.Error as e:
                st.write(f'Erro ao acessar o banco de dados: {e}')
            finally:
                if conexao:
                    conexao.close()  # fecha a conexão com o banco de dados

################################################################################
if botao_precionado:  
    if type_soma == "Por Drop": 
        st.write('## POR DROP')
        with st.spinner('Aguarde Carregando...'):
            time.sleep(2)
            try:
                conexao = sqlite3.connect(DB_PATH)  
                cursor = conexao.cursor()
                consulta_sql = f"""
                SELECT PDROP, SUM(PESOLIQUIDO) as TOTAL_PESOLIQUIDO,
                COUNT(PESOLIQUIDO) as QUANTIDADE_ITENS
                FROM PESAGENS
                WHERE DATA BETWEEN ? AND ?
                AND PESOLIQUIDO > 0.9
                GROUP BY PDROP;
                """
                cursor.execute(consulta_sql, (data_peak_de, data_peak_ate))
                resultados = cursor.fetchall() 
                
                if resultados:
                    mapeamento = {-1: 'NÃO CLASSIFICADO', 1: 'DROP 1', 2: 'DROP 2', 3: 'DROP 3', 4: 'DROP 4', 5: 'DROP 5', 6: 'DROP 6'}
                    resultados_substituidos = [(mapeamento.get(numero, numero), total, quantidade) 
                    for numero, total, quantidade in resultados]

                    df = pd.DataFrame(resultados_substituidos, columns=['DROP (ESTAÇÃO DE QUEDA)', 'PESO TOTAL', 'QUANTIDADE'])
                    st.dataframe(df)
                    st.bar_chart(df[['DROP (ESTAÇÃO DE QUEDA)', 'PESO TOTAL']], x="DROP (ESTAÇÃO DE QUEDA)", y="PESO TOTAL")
                else:
                    st.write('## Nenhum dado encontrado para o período selecionado.')
            except sqlite3.Error as e:
                st.write(f'Erro ao acessar o banco de dados: {e}')
            finally:
                if conexao:
                    conexao.close()  # fecha a conexão com o banco de dados
