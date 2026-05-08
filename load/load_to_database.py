import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def carregar_spotify():

    df_spotify = pd.read_csv(
        "../data/raw/spotify_musicas.csv"
    )

    df_spotify.to_sql(
        "spotify_musicas",
        engine,
        if_exists="append",
        index=False
    )

    print("Spotify carregado com sucesso!")


def carregar_youtube():

    df_youtube = pd.read_csv(
        "../data/raw/youtube_videos.csv"
    )

    df_youtube.to_sql(
        "youtube_videos",
        engine,
        if_exists="append",
        index=False
    )

    print("YouTube carregado com sucesso!")


if __name__ == "__main__":

    carregar_spotify()

    carregar_youtube()

    print("\nCarga finalizada com sucesso!")