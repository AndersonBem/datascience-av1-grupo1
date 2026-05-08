import os
import json
import requests
import pandas as pd

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


def pegar_token_spotify():

    url = "https://accounts.spotify.com/api/token"

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(
        url,
        data=data,
        auth=HTTPBasicAuth(
            CLIENT_ID,
            CLIENT_SECRET
        )
    )

    response.raise_for_status()

    token = response.json()["access_token"]

    return token


def popularidade_por_posicao(posicao):

    faixas = [
        (10, 95),
        (20, 85),
        (30, 75),
        (40, 65),
        (50, 55),
    ]

    for limite, popularidade in faixas:

        if posicao <= limite:
            return popularidade

    return 40


def buscar_musicas_populares():

    token = pegar_token_spotify()

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    musicas = []

    # -----------------------------------------
    # PAGINAÇÃO -> 50 MÚSICAS
    # -----------------------------------------

    for offset in range(0, 50, 10):

        params = {

            "q": "a",

            "type": "track",

            "limit": 10,

            "offset": offset,

            "market": "US" # BR É UMA OPCAO TBM
        }

        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        dados = response.json()

        for index, track in enumerate(
            dados["tracks"]["items"],
            start=offset + 1
        ):

            popularidade_spotify = track.get("popularity")

            musica = {

                # ID ÚNICO DO SPOTIFY
                "id_musica": track["id"],

                "nome_musica": track["name"],

                "artista": track["artists"][0]["name"],

                "album": track["album"]["name"],

                # Se vier null usa popularidade por posição
                "popularidade": (
                    popularidade_spotify
                    if popularidade_spotify is not None
                    else popularidade_por_posicao(index)
                ),

                "duracao": track["duration_ms"],

                "genero": None,

                "data_lancamento": track["album"]["release_date"],

                "playlist_nome": "Spotify Search",

                "playlist_id": "spotify_search"
            }

            musicas.append(musica)

    return musicas


if __name__ == "__main__":

    musicas = buscar_musicas_populares()

    # -----------------------------------------
    # SALVAR JSON
    # -----------------------------------------

    with open(
        "../data/raw/spotify_musicas.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            musicas,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    # -----------------------------------------
    # DATAFRAME
    # -----------------------------------------

    df = pd.DataFrame(musicas)

    print(df.head())

    print(f"\nTotal de músicas: {len(df)}")

    # -----------------------------------------
    # SALVAR CSV
    # -----------------------------------------

    df.to_csv(
        "../data/raw/spotify_musicas.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nJSON e CSV gerados com sucesso!")