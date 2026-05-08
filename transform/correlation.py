import pandas as pd

spotify = pd.read_csv("data/processed/spotify_clean.csv")
youtube = pd.read_csv("data/processed/youtube_clean.csv")

## Todas correlações na lista
correlacoes = []

## Ordenando musicas do spotify
spotify_ordenado = spotify.sort_values(
    by = "popularidade",
    ascending= False
)

## Criar uma popularidade melhor que visualizações
youtube["popularidade_video"] = (
    youtube["visualizacoes"] * 0.5 +
    youtube["likes"] * 0.3 +
    youtube["comentarios"] * 0.2
)

## Ordenando videos do youtube
youtube_ordenado = youtube.sort_values(
    by="popularidade_video",
    ascending=False
)

## A regra estava muito rigida, e estava gerando um correlation.csv vazio
def normalizar_texto(texto):
    return str(texto).strip().lower()

def limpar_nome_musica(nome):
    nome = str(nome)
    nome = nome.split(" - ")[0] 
    nome = nome.split("(")[0] 
    return nome.strip().lower()

for _, musica in spotify_ordenado.iterrows():

    nome_musica = musica["nome_musica"]
    artista = musica["artista"]

    for _, video in youtube_ordenado.iterrows():

        titulo_video = video["titulo_video"]
        canal = video["canal"]
        ## musicas_populares_no_spotify_que_tambem_aparecem_no_youtube
        nome_musica_limpo = limpar_nome_musica(nome_musica)
        titulo_video_limpo = normalizar_texto(titulo_video)

        if nome_musica_limpo in titulo_video_limpo:
            correlacoes.append({
                "musica": nome_musica,
                "titulo_video": titulo_video,
                "artista" : musica["artista"],
                "canal": canal,
                "tipo_correlacao": "musica_popular_em_videos_populares",
                "album": musica["album"],
                "data_lancamento_musica": musica["data_lancamento"],
                "data_lancamento_video": video["data_publicacao"],
                "popularidade_musica": musica["popularidade"],
                "visualizacoes_video": video["visualizacoes"],
                "popularidade_video": video["popularidade_video"]
            })
        ##artistas_populares_nas_duas_plataformas
        artista_limpo = normalizar_texto(artista)
        canal_limpo = normalizar_texto(canal)

        canal_limpo = canal_limpo.replace("vevo", "").replace(" - topic", "").strip()

        if artista_limpo in canal_limpo or canal_limpo in artista_limpo:
            correlacoes.append({
                "musica": nome_musica,
                "titulo_video": titulo_video,
                "artista" : musica["artista"],
                "canal": canal,
                "tipo_correlacao": "artista_popular_nas_duas_plataformas",
                "album": musica["album"],
                "data_lancamento_musica": musica["data_lancamento"],
                "data_lancamento_video": video["data_publicacao"],
                "popularidade_musica": musica["popularidade"],
                "visualizacoes_video": video["visualizacoes"],
                "popularidade_video": video["popularidade_video"]
            })
        

resultado = pd.DataFrame(correlacoes)

resultado.to_csv(
    "data/processed/correlation.csv",
    index=False
)


        