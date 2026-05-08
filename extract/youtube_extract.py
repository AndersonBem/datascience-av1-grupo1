import os
import json
import requests
import pandas as pd

from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def buscar_videos_populares():

    url_search = "https://www.googleapis.com/youtube/v3/search"

    params_search = {
        "part": "snippet",
        "q": "music",
        "type": "video",
        "maxResults": 50,
        "regionCode": "US",  # alterar região aqui
        "key": YOUTUBE_API_KEY
    }

    response_search = requests.get(
        url_search,
        params=params_search
    )

    response_search.raise_for_status()

    dados_search = response_search.json()

    video_ids = []

    for item in dados_search["items"]:

        video_ids.append(
            item["id"]["videoId"]
        )

    # -----------------------------------------
    # BUSCAR DETALHES DOS VÍDEOS
    # -----------------------------------------

    url_videos = "https://www.googleapis.com/youtube/v3/videos"

    params_videos = {
        "part": "snippet,statistics",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }

    response_videos = requests.get(
        url_videos,
        params=params_videos
    )

    response_videos.raise_for_status()

    dados_videos = response_videos.json()

    videos = []

    for item in dados_videos["items"]:

        snippet = item["snippet"]

        statistics = item.get(
            "statistics",
            {}
        )

        visualizacoes = int(
            statistics.get("viewCount", 0)
        )

        likes = int(
            statistics.get("likeCount", 0)
        )

        comentarios = int(
            statistics.get("commentCount", 0)
        )

        engajamento = 0

        if visualizacoes > 0:

            engajamento = (
                (likes + comentarios)
                / visualizacoes
            )

        video = {

            # ID ÚNICO DO YOUTUBE
            "id_video": item["id"],

            "titulo_video": snippet["title"],

            "nome_canal": snippet["channelTitle"],

            "categoria": snippet.get("categoryId"),

            "visualizacoes": visualizacoes,

            "likes": likes,

            "comentarios": comentarios,

            "engajamento": round(
                engajamento,
                4
            ),

            "regiao": "US",

            "data_publicacao": snippet["publishedAt"][:10]
        }

        videos.append(video)

    return videos


if __name__ == "__main__":

    videos = buscar_videos_populares()

    # -----------------------------------------
    # SALVAR JSON
    # -----------------------------------------

    with open(
        "../data/raw/youtube_videos.json",
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            videos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

    # -----------------------------------------
    # DATAFRAME
    # -----------------------------------------

    df = pd.DataFrame(videos)

    print(df.head())

    print(f"\nTotal de vídeos: {len(df)}")

    # -----------------------------------------
    # SALVAR CSV
    # -----------------------------------------

    df.to_csv(
        "../data/raw/youtube_videos.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nCSV gerado com sucesso!")