from pathlib import Path
import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def carregar_spotify():

    df_spotify = pd.read_csv(PROCESSED_DIR / "spotify_clean.csv")

    df_spotify.to_sql(
        "spotify_musicas",
        engine,
        if_exists="append",
        index=False
    )

    print("Spotify carregado com sucesso!")


def carregar_youtube():

    df_youtube = pd.read_csv(PROCESSED_DIR / "youtube_clean.csv")

    df_youtube.to_sql(
        "youtube_videos",
        engine,
        if_exists="append",
        index=False
    )

    print("YouTube carregado com sucesso!")

def carregar_correlacoes():
    df_correlacoes = pd.read_csv(PROCESSED_DIR / "correlation.csv")

    df_correlacoes.to_sql(
        "correlacoes",
        engine,
        if_exists="append",
        index=False
    )

    print("Correlações carregadas com sucesso!")

def limpar_tabelas():
    with engine.begin() as conn:
        conn.execute(text("""
            TRUNCATE TABLE correlacoes, spotify_musicas, youtube_videos
            RESTART IDENTITY CASCADE;
        """))

    print("Tabelas limpas com sucesso!")

if __name__ == "__main__":

    print("\nLimpando tabelas...")
    limpar_tabelas()

    carregar_spotify()

    carregar_youtube()

    carregar_correlacoes()

    print("\nCarga finalizada com sucesso!")