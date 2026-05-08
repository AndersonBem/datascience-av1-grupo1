import os

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_URL = DATABASE_URL

st.set_page_config(page_title="Dashboard Roberto Silva - Grupo 1", layout="wide")

st.title("Dashboard de Tendências: Spotify & YouTube")
st.markdown("Status: **Etapa 2-C** - Visualização Completa e Análise Regional")


@st.cache_data
def carregar_dados_gerais():
    engine = create_engine(POSTGRES_URL)

    df_s = pd.read_sql("SELECT * FROM spotify_musicas", engine)
    df_y = pd.read_sql("SELECT * FROM youtube_videos", engine)
    df_c = pd.read_sql("SELECT * FROM correlacoes", engine)

    st.sidebar.success("Conectado ao Postgres!")

    return df_s, df_y, df_c


df_s, df_y, df_c = carregar_dados_gerais()

df_s["data_lancamento"] = pd.to_datetime(df_s["data_lancamento"])
df_y["data_publicacao"] = pd.to_datetime(df_y["data_publicacao"])

df_y["engajamento"] = (df_y["likes"] + df_y["comentarios"]) / df_y["visualizacoes"]

st.sidebar.header("Filtros do Sistema")

periodo = st.sidebar.date_input(
    "Período",
    [df_s["data_lancamento"].min(), df_s["data_lancamento"].max()]
)

generos = st.sidebar.multiselect(
    "Gêneros Musicais",
    sorted(df_s["genero"].dropna().unique()),
    default=sorted(df_s["genero"].dropna().unique())
)

regioes = st.sidebar.multiselect(
    "Regiões (YouTube)",
    sorted(df_y["regiao"].dropna().unique()),
    default=sorted(df_y["regiao"].dropna().unique())
)

artistas = st.sidebar.multiselect(
    "Artistas Spotify",
    sorted(df_s["artista"].dropna().unique()),
    default=sorted(df_s["artista"].dropna().unique())
)

canais = st.sidebar.multiselect(
    "Canais YouTube",
    sorted(df_y["canal"].dropna().unique()),
    default=sorted(df_y["canal"].dropna().unique())
)

min_eng = st.sidebar.slider(
    "Engajamento Mínimo (YouTube)",
    0.0,
    float(df_y["engajamento"].max() or 1.0),
    0.0
)

if isinstance(periodo, (list, tuple)) and len(periodo) == 2:
    df_s_f = df_s[
        (df_s["data_lancamento"].dt.date >= periodo[0])
        & (df_s["data_lancamento"].dt.date <= periodo[1])
        & (df_s["genero"].isin(generos))
        & (df_s["artista"].isin(artistas))
    ]

    df_y_f = df_y[
        (df_y["data_publicacao"].dt.date >= periodo[0])
        & (df_y["data_publicacao"].dt.date <= periodo[1])
        & (df_y["regiao"].isin(regioes))
        & (df_y["canal"].isin(canais))
        & (df_y["engajamento"] >= min_eng)
    ]

    st.divider()
    st.header("Visão Geral")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top músicas por popularidade")
        top_spotify = df_s_f.nlargest(10, "popularidade")

        st.plotly_chart(
            px.bar(
                top_spotify,
                x="nome_musica",
                y="popularidade",
                color="artista",
                hover_data=["album", "genero", "data_lancamento"],
                title="Top 10 músicas no Spotify"
            ),
            use_container_width=True
        )

    with col2:
        st.subheader("Top vídeos por visualizações")
        top_youtube = df_y_f.nlargest(10, "visualizacoes")

        st.plotly_chart(
            px.bar(
                top_youtube,
                x="titulo_video",
                y="visualizacoes",
                color="canal",
                hover_data=["likes", "comentarios", "engajamento", "regiao"],
                title="Top 10 vídeos no YouTube"
            ),
            use_container_width=True
        )

    st.divider()
    st.header("Correlação entre Spotify e YouTube")

    if not df_c.empty:
        st.subheader("Popularidade Spotify x Popularidade YouTube")

        top_corr = df_c.sort_values(
            by="visualizacoes_video",
            ascending=False
        ).head(10).copy()

        df_barras = top_corr[
            [
                "musica",
                "popularidade_musica",
                "popularidade_video",
                "visualizacoes_video",
                "artista",
                "titulo_video",
                "tipo_correlacao"
            ]
        ]

        df_barras = df_barras.rename(columns={
            "popularidade_musica": "Popularidade Spotify",
            "popularidade_video": "Popularidade YouTube"
        })

        df_barras_melt = df_barras.melt(
            id_vars=[
                "musica",
                "visualizacoes_video",
                "artista",
                "titulo_video",
                "tipo_correlacao"
            ],
            value_vars=[
                "Popularidade Spotify",
                "Popularidade YouTube"
            ],
            var_name="Plataforma",
            value_name="Valor"
        )

        st.plotly_chart(
            px.bar(
                df_barras_melt,
                x="musica",
                y="Valor",
                color="Plataforma",
                barmode="group",
                hover_data=[
                    "artista",
                    "titulo_video",
                    "visualizacoes_video",
                    "tipo_correlacao"
                ],
                title="Comparação entre popularidade no Spotify e força dos vídeos no YouTube"
            ),
            use_container_width=True
        )

        st.subheader("Tabela de correlações encontradas")

        colunas_correlacao = [
            "musica",
            "artista",
            "titulo_video",
            "canal",
            "tipo_correlacao",
            "popularidade_musica",
            "visualizacoes_video",
            "popularidade_video"
        ]

        st.dataframe(
            df_c[colunas_correlacao].sort_values(
                by="visualizacoes_video",
                ascending=False
            ),
            use_container_width=True
        )
    else:
        st.warning("Nenhuma correlação encontrada no banco.")

    st.divider()
    st.header("Consumo Global e Engajamento")

    df_reg = df_y_f.groupby("regiao").agg(
        {
            "visualizacoes": "sum",
            "engajamento": "mean"
        }
    ).reset_index()

    c_map, c_pie = st.columns([2, 1])

    with c_map:
        st.plotly_chart(
            px.choropleth(
                df_reg,
                locations="regiao",
                color="engajamento",
                hover_name="regiao",
                color_continuous_scale="Viridis",
                title="Engajamento por País"
            ),
            use_container_width=True
        )

    with c_pie:
        st.plotly_chart(
            px.pie(
                df_reg,
                values="visualizacoes",
                names="regiao",
                hole=0.4,
                title="Visualizações por Região"
            ),
            use_container_width=True
        )

    st.divider()
    st.header("Tabelas Interativas")

    t_m, t_v, t_c, t_corr = st.tabs(
        ["Músicas", "Vídeos", "Resumo por Região", "Correlações"]
    )

    with t_m:
        st.dataframe(
            df_s_f.sort_values(by="popularidade", ascending=False),
            use_container_width=True
        )

    with t_v:
        st.dataframe(
            df_y_f.sort_values(by="visualizacoes", ascending=False),
            use_container_width=True
        )

    with t_c:
        st.write("Métricas consolidadas por território:")
        st.dataframe(
            df_reg.sort_values(by="engajamento", ascending=False),
            use_container_width=True
        )

    with t_corr:
        st.dataframe(
            df_c.sort_values(by="visualizacoes_video", ascending=False),
            use_container_width=True
        )

else:
    st.info("Selecione o intervalo de datas completo no menu lateral.")