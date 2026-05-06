import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from pymongo import MongoClient
import certifi

# --- CONFIGS DE CONEXÃO ---
POSTGRES_URL = "postgresql://neondb_owner:npg_TLsk8N9ODFBU@ep-bold-glitter-aqrzonw8-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
MONGO_URI = "" 

st.set_page_config(page_title="Dashboard Roberto Silva - Grupo 1", layout="wide")

st.title(" Dashboard de Tendências: Spotify & YouTube")
st.markdown("Status: **Etapa 2-C** - Visualização Completa e Análise Regional")

@st.cache_data
def carregar_dados_gerais():
    try:
        engine = create_engine(POSTGRES_URL)
        df_s = pd.read_sql("SELECT * FROM musicas", engine)
        df_y = pd.read_sql("SELECT * FROM videos", engine)
        st.sidebar.success(" Conectado ao Postgres (Neon)!")
        return df_s, df_y
    except Exception as e:
        print(f"Erro Postgres: {e}")
        pass 

    # Dados de teste 
    data_s = {
        "nome_musica": [f"Música {i}" for i in range(1, 51)],
        "artista": ["Slayer", "Metallica", "Iron Maiden", "Anitta", "Alok"] * 10,
        "popularidade": [95, 80, 85, 70, 60] * 10,
        "genero": ["Metal", "Metal", "Metal", "Pop", "Eletrônica"] * 10,
        "data_lancamento": pd.date_range(start="2024-01-01", periods=50)
    }
    data_y = {
        "titulo_video": [f"Vídeo {i}" for i in range(1, 51)],
        "canal": ["Slayer", "Metallica", "Iron Maiden", "Anitta", "Alok"] * 10,
        "visualizacoes": [1000000, 500000, 800000, 1200000, 300000] * 10,
        "likes": [50000, 20000, 35000, 60000, 15000] * 10,
        "comentarios": [5000, 2000, 3000, 4000, 1000] * 10,
        "regiao": ["BRA", "USA", "GBR", "BRA", "JPN"] * 10,
        "data_publicacao": pd.date_range(start="2024-01-01", periods=50)
    }
    return pd.DataFrame(data_s), pd.DataFrame(data_y)

# Processamento
df_s, df_y = carregar_dados_gerais()
df_s['data_lancamento'] = pd.to_datetime(df_s['data_lancamento'])
df_y['data_publicacao'] = pd.to_datetime(df_y['data_publicacao'])
df_y['engajamento'] = (df_y['likes'] + df_y['comentarios']) / df_y['visualizacoes']

#  SIDEBAR 
st.sidebar.header("Filtros do Sistema")
periodo = st.sidebar.date_input(" Período", [df_s['data_lancamento'].min(), df_s['data_lancamento'].max()])
generos = st.sidebar.multiselect(" Gêneros Musicais", df_s['genero'].unique(), default=df_s['genero'].unique())
regioes = st.sidebar.multiselect("Regiões (YouTube)", df_y['regiao'].unique(), default=df_y['regiao'].unique())
artistas = st.sidebar.multiselect("Artistas/Canais", df_s['artista'].unique(), default=df_s['artista'].unique())
min_eng = st.sidebar.slider(" Engajamento Mínimo (YouTube)", 0.0, float(df_y['engajamento'].max() or 1.0), 0.0)

if isinstance(periodo, (list, tuple)) and len(periodo) == 2:
    # Filtragem
    df_s_f = df_s[(df_s['data_lancamento'].dt.date >= periodo[0]) & (df_s['data_lancamento'].dt.date <= periodo[1]) & (df_s['genero'].isin(generos)) & (df_s['artista'].isin(artistas))]
    df_y_f = df_y[(df_y['data_publicacao'].dt.date >= periodo[0]) & (df_y['data_publicacao'].dt.date <= periodo[1]) & (df_y['regiao'].isin(regioes)) & (df_y['canal'].isin(artistas)) & (df_y['engajamento'] >= min_eng)]

    #  TOP 10 
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Top 10 Spotify")
        # Invertido: nome da musica no X e popularidade no Y para ficar na vertical
        st.plotly_chart(px.bar(df_s_f.nlargest(10, 'popularidade'), x='nome_musica', y='popularidade', color='artista'), use_container_width=True)
    with col2:
        st.subheader(" Top 10 YouTube")
        # Invertido: nome da musica no X e popularidade no Y para ficar na vertical
        st.plotly_chart(px.bar(df_y_f.nlargest(10, 'visualizacoes'), x='titulo_video', y='visualizacoes', color='canal'), use_container_width=True)

    #  ANÁLISE REGIONAL 
    st.divider()
    st.header(" Consumo Global e Engajamento")
    df_reg = df_y_f.groupby('regiao').agg({'visualizacoes': 'sum', 'engajamento': 'mean'}).reset_index()
    
    c_map, c_pie = st.columns([2, 1])
    with c_map:
        st.plotly_chart(px.choropleth(df_reg, locations="regiao", color="engajamento", hover_name="regiao", color_continuous_scale="Viridis", title="Engajamento por País"), use_container_width=True)
    with c_pie:
        st.plotly_chart(px.pie(df_reg, values='visualizacoes', names='regiao', hole=0.4, title="Visualizações por Região"), use_container_width=True)

    # TABELAS INTERATIVAS 
    st.divider()
    st.header(" Tabelas Interativas")
    t_m, t_v, t_c = st.tabs(["Músicas", "Vídeos", " Resumo por Região"])

    with t_m:
        st.dataframe(df_s_f.sort_values(by='popularidade', ascending=False), use_container_width=True)
    with t_v:
        st.dataframe(df_y_f.sort_values(by='visualizacoes', ascending=False), use_container_width=True)
    with t_c:
        st.write("Métricas consolidadas por território:")
        st.dataframe(df_reg.sort_values(by='engajamento', ascending=False), use_container_width=True)
else:
    st.info("Selecione o intervalo de datas completo no menu lateral.")