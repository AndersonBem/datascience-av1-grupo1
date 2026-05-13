import pandas as pd
import os
from pathlib import Path

os.makedirs("../data/processed", exist_ok=True)
BASE_DIR = Path(__file__).resolve().parent.parent
arquivo_json = BASE_DIR / "data" / "processed" / "spotify_clean.json"
arquivo_csv = BASE_DIR / "data" / "processed" / "spotify_clean.csv"

arquivo_csv_musicas = BASE_DIR / "data" / "raw" / "spotify_musicas.csv"

# =========================
# SPOTIFY
# =========================

spotify = pd.read_csv(arquivo_csv_musicas)

spotify = spotify.rename(columns={
    "duracao": "duracao_ms"
})

spotify = spotify.dropna(subset=["nome_musica"])
spotify["genero"] = spotify["genero"].fillna("Não informado")
spotify["popularidade"] = pd.to_numeric(spotify["popularidade"], errors="coerce").fillna(0).astype(int)
spotify["duracao_ms"] = pd.to_numeric(spotify["duracao_ms"], errors="coerce").fillna(0).astype(int)
spotify["data_lancamento"] = pd.to_datetime(spotify["data_lancamento"], format="mixed", errors="coerce")

colunas_spotify = [
    "id_musica",
    "nome_musica",
    "artista",
    "album",
    "popularidade",
    "duracao_ms",
    "genero",
    "data_lancamento",
    "playlist_nome",
    "playlist_id"
]

spotify = spotify[colunas_spotify]
spotify = spotify.drop_duplicates(subset=["id_musica"])

spotify.to_csv(
    arquivo_csv,
    sep=",",
    index=False,
    encoding="utf-8-sig"
)



print("Transformação concluída com sucesso!")
print("Arquivos gerados:")
print("../data/processed/spotify_clean.csv")
