from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

youtube = pd.read_csv(RAW_DIR / "youtube_videos.csv")

youtube = youtube.rename(columns={
    "nome_canal": "canal"
})

if "engajamento" not in youtube.columns:
    youtube["engajamento"] = (
        (youtube["likes"] + youtube["comentarios"]) / youtube["visualizacoes"]
    )

colunas_finais = [
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

youtube = youtube[colunas_finais]

youtube = youtube.drop_duplicates(subset=["id_video"])

youtube.to_csv(
    PROCESSED_DIR / "youtube_clean.csv",
    index=False,
    encoding="utf-8"
)

print("youtube_clean.csv gerado com sucesso!")