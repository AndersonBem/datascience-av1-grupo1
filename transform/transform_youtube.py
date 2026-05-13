from pathlib import Path

import pandas as pd
import os

os.makedirs("../data/processed", exist_ok=True)
BASE_DIR = Path(os.path.abspath(__file__)).parent.parent
arquivo_json = BASE_DIR / "data" / "processed" / "youtube_clean.json"
arquivo_csv = BASE_DIR / "data" / "processed" / "youtube_clean.csv"

arquivo_csv_videos = BASE_DIR / "data" / "raw" / "youtube_videos.csv"

# =========================
# YOUTUBE
# =========================

youtube = pd.read_csv(arquivo_csv_videos)

youtube = youtube.rename(columns={
    "nome_canal": "canal"
})

youtube = youtube.dropna(subset=["titulo_video"])
youtube["categoria"] = youtube["categoria"].fillna("Não informado")

youtube["visualizacoes"] = pd.to_numeric(youtube["visualizacoes"], errors="coerce").fillna(0).astype(int)
youtube["likes"] = pd.to_numeric(youtube["likes"], errors="coerce").fillna(0).astype(int)
youtube["comentarios"] = pd.to_numeric(youtube["comentarios"], errors="coerce").fillna(0).astype(int)

youtube["data_publicacao"] = pd.to_datetime(youtube["data_publicacao"], format="mixed", errors="coerce")

colunas_youtube = [
    "id_video",
    "titulo_video",
    "canal",
    "categoria",
    "visualizacoes",
    "likes",
    "comentarios",
    "engajamento",
    "data_publicacao",
    "regiao"
]

youtube = youtube[colunas_youtube]
youtube = youtube.drop_duplicates()

youtube.to_csv(
    arquivo_csv,
    sep=",",
    index=False,
    encoding="utf-8-sig"
)


print("Transformação concluída com sucesso!")
print("Arquivos gerados:")
print(arquivo_csv)