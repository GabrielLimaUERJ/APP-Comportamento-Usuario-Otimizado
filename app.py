# =========================================
# IMPORTS
# =========================================
import streamlit as st
import pandas as pd
import numpy as np
import duckdb
import random
from datetime import datetime, timedelta
import plotly.express as px

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Análise de Conversão de Usuários",
    layout="wide"
)

st.title("📊 Análise de Conversão de Usuários")

# =========================================
# FUNÇÃO DE GERAÇÃO DE DADOS
# =========================================
def gerar_dados(num_users=3000):

    np.random.seed(42)
    random.seed(42)

    eventos = []
    event_id = 1

    origens = ["google", "instagram", "facebook", "direto"]
    devices = ["mobile", "desktop"]

    start_date = datetime(2025, 1, 1)

    # Loop por usuário
    for user_id in range(1, num_users + 1):

        visitas = np.random.poisson(2) + 1

        for _ in range(visitas):

            data = start_date + timedelta(days=random.randint(0, 60))
            origem = random.choice(origens)
            device = random.choice(devices)

            # VISITA
            eventos.append([
                event_id, user_id, data, "visita", origem, device
            ])
            event_id += 1

            # CLIQUE (40%)
            if random.random() < 0.4:
                eventos.append([
                    event_id, user_id, data, "clique", origem, device
                ])
                event_id += 1

                # COMPRA (25%)
                if random.random() < 0.25:
                    eventos.append([
                        event_id, user_id, data, "compra", origem, device
                    ])
                    event_id += 1

    df = pd.DataFrame(eventos, columns=[
        "event_id",
        "user_id",
        "data_evento",
        "etapa",
        "origem_trafego",
        "device"
    ])

    return df


# =========================================
# BOTÃO DE SIMULAÇÃO
# =========================================
if "df" not in st.session_state:
    st.session_state.df = gerar_dados()

if st.button("🔄 Gerar nova simulação"):
    st.session_state.df = gerar_dados()

df = st.session_state.df

# =========================================
# ANÁLISE COM DUCKDB
# =========================================
con = duckdb.connect()
con.execute("CREATE OR REPLACE TABLE eventos AS SELECT * FROM df")

# =========================================
# FUNIL
# =========================================
funil = con.execute("""
SELECT 
  etapa,
  COUNT(DISTINCT user_id) AS usuarios
FROM eventos
GROUP BY etapa
ORDER BY 
  CASE 
    WHEN etapa = 'visita' THEN 1
    WHEN etapa = 'clique' THEN 2
    WHEN etapa = 'compra' THEN 3
  END
""").fetchdf()

# =========================================
# MÉTRICAS DE CONVERSÃO
# =========================================
conversao = con.execute("""
SELECT 
  COUNT(DISTINCT CASE WHEN etapa = 'visita' THEN user_id END) AS visitas,
  COUNT(DISTINCT CASE WHEN etapa = 'clique' THEN user_id END) AS cliques,
  COUNT(DISTINCT CASE WHEN etapa = 'compra' THEN user_id END) AS compras
FROM eventos
""").fetchdf()

visitas = conversao["visitas"][0]
cliques = conversao["cliques"][0]
compras = conversao["compras"][0]

taxa_total = compras / visitas
taxa_clique = cliques / visitas
taxa_compra = compras / cliques if cliques > 0 else 0

# =========================================
# KPIs
# =========================================
col1, col2, col3 = st.columns(3)

col1.metric("Taxa Total", f"{taxa_total:.2%}")
col2.metric("Visita → Clique", f"{taxa_clique:.2%}")
col3.metric("Clique → Compra", f"{taxa_compra:.2%}")

# =========================================
# FUNIL (PLOTLY)
# =========================================
st.subheader("Funil de Conversão")

fig_funil = px.funnel(
    funil,
    x="usuarios",
    y="etapa",
    title="Funil de Conversão"
)

# Remover fundo branco
fig_funil.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig_funil, use_container_width=True)

# =========================================
# CONVERSÃO POR ORIGEM
# =========================================
origem = con.execute("""
SELECT 
  origem_trafego,
  COUNT(DISTINCT CASE WHEN etapa = 'visita' THEN user_id END) AS visitas,
  COUNT(DISTINCT CASE WHEN etapa = 'compra' THEN user_id END) AS compras
FROM eventos
GROUP BY origem_trafego
""").fetchdf()

origem["taxa"] = origem["compras"] / origem["visitas"]

# Ordenar do maior para o menor
origem = origem.sort_values(by="taxa", ascending=False)

st.subheader("Conversão por Origem")
st.bar_chart(origem.set_index("origem_trafego")["taxa"])

# =========================================
# CONVERSÃO POR DEVICE
# =========================================
device = con.execute("""
SELECT 
  device,
  COUNT(DISTINCT CASE WHEN etapa = 'visita' THEN user_id END) AS visitas,
  COUNT(DISTINCT CASE WHEN etapa = 'compra' THEN user_id END) AS compras
FROM eventos
GROUP BY device
""").fetchdf()

device["taxa"] = device["compras"] / device["visitas"]

# Ordenar
device = device.sort_values(by="taxa", ascending=False)

st.subheader("Conversão por Device")
st.bar_chart(device.set_index("device")["taxa"])

# =========================================
# INSIGHTS AUTOMÁTICOS
# =========================================
drop_off = 1 - taxa_compra

st.markdown(f"""
### 🧠 Insight

- Taxa total de conversão: **{taxa_total:.2%}**
- Maior perda ocorre na etapa final (**{drop_off:.2%} de drop-off**)
- Indica possível fricção no processo de compra
""")