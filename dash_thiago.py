import streamlit as st
import pandas as pd
import plotly.express as px
import time

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(
    page_title="Mini Estação Meteorológica",
    page_icon="🌦️",
    layout="wide"
)

# ==========================================================
# TÍTULO
# ==========================================================
st.title("🌦️ Estação Meteorológica - Prof. Thiago")
st.write(
    "Dashboard para acompanhamento das condições ambientais "
    "registradas pela estação."
)

# ==========================================================
# CARREGAMENTO DOS DADOS (COM TRATAMENTO DE ERRO)
# ==========================================================
try:
    df = pd.read_csv("dados_estacao_3.csv")
except FileNotFoundError:
    # Se o arquivo ainda não existir, cria um DataFrame vazio com as colunas
    df = pd.DataFrame(columns=["data_hora", "temperatura", "umidade", "luminosidade_pct"])

# ==========================================================
# PREVENÇÃO DE QUEBRA: VERIFICA SE O CSV ESTÁ VAZIO
# ==========================================================
if df.empty:
    st.warning("Aguardando os primeiros dados do ESP32 chegarem via MQTT...")
    # Como não há dados, já acionamos o recarregamento aqui e paramos a execução visual do resto
    time.sleep(5)
    st.rerun()
else:
    # ==========================================================
    # TRATAMENTO DOS DADOS
    # ==========================================================
    # Atualizado o format para incluir os segundos (%S)
    df["data_hora"] = pd.to_datetime(
        df["data_hora"],
        format="%d/%m/%Y %H:%M:%S"
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
    # Ajustado para exibir 1 casa decimal (.1f) agora que a luminosidade é float
    col3.metric(
        label="☀️ Luminosidade",
        value=f"{luminosidade_atual:.1f} %"
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
    # Ajustado para decimal
    col5.metric(
        "Luminosidade máxima",
        f"{luminosidade_max:.1f} %"
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

    # ==========================================================
    # ATUALIZAÇÃO AUTOMÁTICA (Movido para o final)
    # ==========================================================
    # Garante que os gráficos sejam renderizados primeiro, 
    # depois aguarda 5 segundos para recarregar a tela.
    time.sleep(5)
    st.rerun()