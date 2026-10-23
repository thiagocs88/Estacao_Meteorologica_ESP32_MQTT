import streamlit as st
import pandas as pd
import plotly.express as px
import time # <--- Importe a biblioteca de tempo nativa do Python

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Mini Estação Meteorológica",
    page_icon="🌦️",
    layout="wide"
)

time.sleep(5)
st.rerun()
# ==========================================================
# TÍTULO
# ==========================================================
st.title("🌦️ Mini Estação Meteorológica")
st.write(
    "Dashboard para acompanhamento das condições ambientais "
    "registradas pela estação."
)
# ==========================================================
# CARREGAMENTO DOS DADOS
# ==========================================================
df = pd.read_csv("dados_estacao.csv")
# ==========================================================
# TRATAMENTO DOS DADOS
# ==========================================================
df["data_hora"] = pd.to_datetime(
    df["data_hora"],
    format="%d/%m/%Y %H:%M"
)
# ==========================================================
# ÚLTIMA LEITURA
# ==========================================================
ultima_leitura = df.iloc[-1]
temperatura_atual = ultima_leitura["temperatura"]
umidade_atual = ultima_leitura["umidade"]
luminosidade_atual = ultima_leitura["luminosidade_pct"]
# ==========================================================
# INDICADORES ATUAIS
# ==========================================================
st.subheader("Condições atuais")
col1, col2, col3 = st.columns(3)
col1.metric(
    label="🌡️ Temperatura",
    value=f"{temperatura_atual:.1f} °C"
)
col2.metric(
    label="💧 Umidade",
    value=f"{umidade_atual:.1f} %"
)
col3.metric(
    label="☀️ Luminosidade",
    value=f"{luminosidade_atual:.0f} %"
)
# ==========================================================
# GRÁFICOS
# ==========================================================
st.subheader("Evolução das medições")
# ----------------------------------------------------------
# Temperatura
# ----------------------------------------------------------
fig_temp = px.line(
    df,
    x="data_hora",
    y="temperatura",
    markers=True,
    title="🌡️ Temperatura ao longo do tempo",
    labels={
        "data_hora": "Data / Hora",
        "temperatura": "Temperatura (°C)"
    }
)
# ----------------------------------------------------------
# Umidade
# ----------------------------------------------------------
fig_umidade = px.line(
    df,
    x="data_hora",
    y="umidade",
    markers=True,
    title="💧 Umidade ao longo do tempo",
    labels={
        "data_hora": "Data / Hora",
        "umidade": "Umidade (%)"
    }
)
# ----------------------------------------------------------
# Exibição lado a lado
# ----------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(
        fig_temp,
        use_container_width=True
    )
with col2:
    st.plotly_chart(
        fig_umidade,
        use_container_width=True
    )
# ----------------------------------------------------------
# Luminosidade
# ----------------------------------------------------------
fig_luminosidade = px.line(
    df,
    x="data_hora",
    y="luminosidade_pct",
    markers=True,
    title="☀️ Luminosidade ao longo do tempo",
    labels={
        "data_hora": "Data / Hora",
        "luminosidade_pct": "Luminosidade (%)"
    }
)
st.plotly_chart(
    fig_luminosidade,
    use_container_width=True
)
# ==========================================================
# RESUMO DO PERÍODO
# ==========================================================
st.subheader("📊 Resumo do período")
temp_min = df["temperatura"].min()
temp_media = df["temperatura"].mean()
temp_max = df["temperatura"].max()
umidade_media = df["umidade"].mean()
luminosidade_max = df["luminosidade_pct"].max()
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(
    "Temperatura mínima",
    f"{temp_min:.1f} °C"
)
col2.metric(
    "Temperatura média",
    f"{temp_media:.1f} °C"
)
col3.metric(
    "Temperatura máxima",
    f"{temp_max:.1f} °C"
)
col4.metric(
    "Umidade média",
    f"{umidade_media:.1f} %"
)
col5.metric(
    "Luminosidade máxima",
    f"{luminosidade_max:.0f} %"
)
# ==========================================================
# HISTÓRICO
# ==========================================================
st.subheader("📋 Histórico de leituras")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
