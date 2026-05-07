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

            # ALTERAR MERCADO AQUI
            # BR = Brasil
            # US = Estados Unidos
            # JP = Japão
            # ES = Espanha
            "market": "US"
        }

        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        response.raise_for_status()

        dados = response.json()

        for track in dados["tracks"]["items"]:

            musica = {

                # ID ÚNICO DO SPOTIFY
                "id_musica": track["id"],

                "nome_musica": track["name"],

                "artista": track["artists"][0]["name"],

                "album": track["album"]["name"],

                # NULL se não existir
                "popularidade": track.get("popularity"),

                # nome da coluna igual ao banco
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