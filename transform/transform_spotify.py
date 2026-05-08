from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

spotify = pd.read_csv(RAW_DIR / "spotify_musicas.csv")

spotify = spotify.rename(columns={
    "duracao": "duracao_ms"
})

colunas_finais = [
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

def corrigir_data_spotify(data):
    if pd.isna(data):
        return None

    data = str(data)

    if len(data) == 4:
        return f"{data}-01-01"

    return data

spotify = spotify[colunas_finais]

spotify["genero"] = spotify["genero"].fillna("Não informado")

spotify["data_lancamento"] = spotify["data_lancamento"].apply(corrigir_data_spotify)

spotify = spotify.drop_duplicates(subset=["id_musica"])



spotify.to_csv(
    PROCESSED_DIR / "spotify_clean.csv",
    index=False,
    encoding="utf-8"
)

print("spotify_clean.csv gerado com sucesso!")