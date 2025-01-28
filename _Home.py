import streamlit as st
import time
import pandas as pd
import requests
from io import StringIO
import altair as alt

st.set_page_config(
    page_title="Home",
    page_icon="📆",
)

st.sidebar.markdown("Db_Temperaturas")
st.title(':red[RELATÓRIOS DE TEMPERATURAS]')
st.write("BY TALIS")

st.sidebar.header("Selecione a data")

data_inicial = st.sidebar.date_input('DATA:', format="DD/MM/YYYY")
if data_inicial:
    data_peak = data_inicial.strftime('%d%b%Y')

botao_precionado = st.sidebar.button(':blue[Carregar Dados]')

# Inicializa o estado da aplicação para armazenar sensores e dados
if "sensores_selecionados" not in st.session_state:
    st.session_state["sensores_selecionados"] = []
if "df_completo" not in st.session_state:
    st.session_state["df_completo"] = pd.DataFrame()

# Função para carregar os dados e preencher o DataFrame
def carregar_dados():
    # Monta a URL com o timestamp
    url = f"http://192.168.0.4:81/data?time={data_peak}"
    response = requests.get(url)

    if response.status_code == 200:
        csv_data = response.text
        df = pd.read_csv(StringIO(csv_data))
        df.columns = ["DISPOSITIVO", "SENSOR_NOME", "VALOR", "TIMESTAMP"]

        # Ajustar o TIMESTAMP
        df["TIMESTAMP"] = pd.to_datetime(df["TIMESTAMP"], unit="ms")
        df["TIMESTAMP"] = df["TIMESTAMP"].dt.tz_localize('UTC').dt.tz_convert('America/Sao_Paulo')
        df["TIMESTAMP"] = df["TIMESTAMP"].dt.strftime('%Y-%m-%d %H:%M:%S')

        st.session_state["df_completo"] = df  # Salva o DataFrame no estado
        st.success("Dados carregados com sucesso!")
    else:
        st.error(f"Erro ao carregar dados: {response.status_code}")

# Carregar os dados ao pressionar o botão
if botao_precionado:
    with st.spinner('Aguarde enquanto os dados são carregados...'):
        time.sleep(2)
        carregar_dados()

# Exibe os checkboxes e permite selecionar sensores
if not st.session_state["df_completo"].empty:
    df = st.session_state["df_completo"]

    # Criação dos checkboxes
    st.header("Selecione os Sensores")
    sensores = df["SENSOR_NOME"].unique()

    for sensor in sensores:
        # Usar `st.session_state` para persistir a seleção dos checkboxes
        if sensor not in st.session_state:
            st.session_state[sensor] = False

        # Checkbox para cada sensor
        st.session_state[sensor] = st.checkbox(sensor, value=st.session_state[sensor])

    # Atualiza a lista de sensores selecionados
    st.session_state["sensores_selecionados"] = [
        sensor for sensor in sensores if st.session_state[sensor]
    ]

    # Botão para gerar o gráfico
    if st.button(':blue[Gerar gráfico]'):
        if st.session_state["sensores_selecionados"]:
            # Filtrar os dados com base nos sensores selecionados
            sensores_selecionados = st.session_state["sensores_selecionados"]
            df_filtrado = df[df["SENSOR_NOME"].isin(sensores_selecionados)]
            
            # Criar gráfico interativo
            st.header(":bar_chart: Gráfico Interativo de Sensores Selecionados")
            hover = alt.selection_single(
                fields=["TIMESTAMP"],
                nearest=True,
                on="mouseover",
                empty="none",
            )
            valor_maximo = df_filtrado["VALOR"].max()
            valor_minimo = df_filtrado["VALOR"].min()
            linhas = (
                alt.Chart(df_filtrado)
                .mark_line()
                .encode(
                    x=alt.X("TIMESTAMP:T", title="Hora", axis=alt.Axis(format="%H:%M:%S")),  # Formato de hora
                    y=alt.Y("VALOR:Q", title="Temperatura ºC", scale=alt.Scale(domain=[valor_minimo, valor_maximo])),
                    color=alt.Color("SENSOR_NOME:N", title="Sensor"),
                )
            )

            pontos = linhas.transform_filter(hover).mark_circle(size=65)

            tooltips = (
                alt.Chart(df_filtrado)
                .mark_rule()
                .encode(
                    x="TIMESTAMP:T",
                    y="VALOR:Q",
                    opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                    tooltip=[
                        alt.Tooltip("TIMESTAMP:T", title="Timestamp"),
                        alt.Tooltip("SENSOR_NOME:N", title="Sensor"),
                        alt.Tooltip("VALOR:Q", title="Valor"),
                    ],
                )
                .add_selection(hover)
            )

            grafico = linhas + pontos + tooltips
            st.altair_chart(grafico, use_container_width=True)
            # Exibir tabela filtrada
            st.header("Tabela Filtrada")
            st.dataframe(df_filtrado, height=350,width=600 ) 
        else:
            st.warning("Nenhum sensor selecionado. Por favor, selecione pelo menos um sensor.")
else:
    st.info("Carregue os dados para visualizar os sensores disponíveis.")
