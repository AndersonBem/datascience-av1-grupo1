import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from pymongo import MongoClient
import certifi

# CONFIGURAÇÕES DE CONEXÃO 
# Se a gente for de MongoDB na nuvem, colo o link aqui
MONGO_URI = "----------------"

# Se a gente for usar o Postgres local
POSTGRES_URL = "--------------"

# Deixando a página larga pra os gráficos não ficarem espremidos
st.set_page_config(page_title="Dashboard Lucas - Grupo 1", layout="wide")

st.title("Dashboard de Tendências: Spotify & YouTube")
st.markdown(" Visualização funcionando!")

@st.cache_data
def carregar_dados():
    # 1ª TENTATIVA: Tenta puxar do Postgres 
    try:
        engine = create_engine(POSTGRES_URL)
        df_s = pd.read_sql("SELECT * FROM musicas", engine)
        df_y = pd.read_sql("SELECT * FROM videos", engine)
        st.sidebar.success("Conectado no Postgres!")
        return df_s, df_y
    except:
        pass 

    # 2ª TENTATIVA: Tenta puxar do MongoDB (Se for usar nuvem)
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client['nome_do_banco']
        df_s = pd.DataFrame(list(db.musicas.find()))
        df_y = pd.DataFrame(list(db.videos.find()))
        
        if not df_s.empty:
            st.sidebar.success("Conectado no MongoDB!")
            return df_s, df_y
    except:
        pass

    # PLANO B: Se der errado, vai carregar os  dados de teste
    st.sidebar.warning(" Bancos offline. Rodando meus dados de teste.")
    
    # Gerando as 50 músicas que o professor pediu
    data_s = {
        "nome_musica": [f"Música {i}" for i in range(1, 51)],
        "artista": ["Slayer", "Metallica", "Iron Maiden", "Megadeth", "Pantera"] * 10,
        "popularidade": [90, 85, 80, 75, 70] * 10,
        "genero": ["Metal"] * 50
    }
    
    # Gerando os 50 vídeos 
    data_y = {
        "titulo_video": [f"Vídeo {i}" for i in range(1, 51)],
        "canal": ["Slayer", "Metallica", "Iron Maiden", "Megadeth", "Pantera"] * 10,
        "visualizacoes": [1000000, 800000, 500000, 300000, 200000] * 10,
        "likes": [50000, 30000, 20000, 15000, 10000] * 10,
        "comentarios": [5000, 3000, 2000, 1000, 500] * 10,
        "regiao": ["BR"] * 50
    }
    return pd.DataFrame(data_s), pd.DataFrame(data_y)

# aqui está puxando os dados 
df_s, df_y = carregar_dados()

# Calculando a métrica de engajamento que o professor exigiu
df_y['engajamento'] = (df_y['likes'] + df_y['comentarios']) / df_y['visualizacoes']

# PARTE VISUAL 

st.sidebar.header("Filtros")
artistas = df_s['artista'].unique()
sel = st.sidebar.multiselect("Escolha os artistas", artistas, default=artistas)

# Dividindo a tela em duas colunas 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Músicas - Popularidade[cite: 2]")
    fig1 = px.bar(df_s[df_s['artista'].isin(sel)].nlargest(10, 'popularidade'), 
                  x='popularidade', y='nome_musica', color='artista', orientation='h')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Vídeos mais vistos no YouTube[cite: 2]")
    fig2 = px.pie(df_y[df_y['canal'].isin(sel)].nlargest(5, 'visualizacoes'), 
                  values='visualizacoes', names='titulo_video', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Gráfico de engajamento pra fechar as métricas 
st.subheader("Análise de Engajamento por Canal")
fig3 = px.box(df_y[df_y['canal'].isin(sel)], x='canal', y='engajamento', color='canal')
st.plotly_chart(fig3, use_container_width=True)

# Mostrando a tabela pra visualizar que os dados 
st.subheader(" Tabela de Dados (Populados)")
st.dataframe(df_s[df_s['artista'].isin(sel)], use_container_width=True)