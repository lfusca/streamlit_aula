import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()
API_URL = os.getenv("API_URL")

st.title("Visualização de Dados do Sensor")

# Inputs de data e hora
col1, col2 = st.columns(2)
with col1:
    data_inicial = st.date_input("Data inicial", value=datetime.now())
with col2:
    data_final = st.date_input("Data final", value=datetime.now())

# Botão de atualização
if st.button("Atualizar"):
    try:
        resposta = requests.get(API_URL)

        if resposta.status_code == 200:
            dados = resposta.json()
            df = pd.DataFrame(dados)

            # Converte tipos
            df["DATA"] = pd.to_datetime(df["DATA"])
            df["DATA_HORA"] = pd.to_datetime(df["DATA"].astype(str) + " " + df["HORA"])

            # Filtra intervalo
            mask = (df["DATA"].dt.date >= data_inicial) & (df["DATA"].dt.date <= data_final)
            df_filtrado = df.loc[mask].sort_values("DATA_HORA")

            if not df_filtrado.empty:
                # Tabela em ordem desejada
                st.subheader("📋 Tabela de Dados")
                st.dataframe(df_filtrado[["DATA", "HORA", "NOME_SENSOR", "VALOR"]])

                # Gráfico com eixo X baseado em DATA_HORA
                st.subheader("📈 Gráfico - Valor por Hora")
                fig = px.line(
                    df_filtrado,
                    x="DATA_HORA",
                    y="VALOR",
                    title="Variação dos Valores ao Longo das Horas",
                    labels={"DATA_HORA": "Data e Hora", "VALOR": "Valor"}
                )
                st.plotly_chart(fig)
            else:
                st.warning("Nenhum dado encontrado no intervalo selecionado.")
        else:
            st.error(f"Erro ao acessar a API: {resposta.status_code}")
    except Exception as e:
        st.error(f"Erro: {e}")