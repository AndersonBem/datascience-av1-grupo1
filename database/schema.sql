CREATE TABLE spotify_musicas (
    id_musica VARCHAR(255) PRIMARY KEY, 
    nome_musica VARCHAR(255) NOT NULL,
    artista VARCHAR(255) NOT NULL,
    album VARCHAR(255),
    popularidade INTEGER,
    duracao INTEGER, 
    genero VARCHAR(100),
    data_lancamento DATE,
    playlist_nome VARCHAR(255),
    playlist_id VARCHAR(255)
);

CREATE TABLE youtube_videos (
    id_video VARCHAR(255) PRIMARY KEY,
    titulo_video VARCHAR(255) NOT NULL,
    nome_canal VARCHAR(255) NOT NULL,
    categoria VARCHAR(100),
    visualizacoes BIGINT,
    likes BIGINT,
    comentarios BIGINT,
    engajamento FLOAT, 
    regiao VARCHAR(50),
    data_publicacao DATE
);

CREATE TABLE correlacoes (
    id_correlacao SERIAL PRIMARY KEY,
    id_musica VARCHAR(255) REFERENCES spotify_musicas(id_musica),
    id_video VARCHAR(255) REFERENCES youtube_videos(id_video),
    tipo_correlacao VARCHAR(100) NOT NULL,
    valor_contratado VARCHAR(255),
    popularidade_spotify INTEGER,
    visualizacoes_youtube BIGINT,
    pontuacao_correlacao NUMERIC(10,4),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);