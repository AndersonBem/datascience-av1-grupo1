CREATE TABLE spotify_musicas (
  id_musica SERIAL PRIMARY KEY,
  nome_musica VARCHAR(255) NOT NULL,
  artista VARCHAR(255) NOT NULL,
  popularidade INTEGER,
  duracap INTEGER,
  data_lancamento DATE,
  nome_playlist VARCHAR(100),
  id_playlist VARCHAR(100)
  
);

CREATE TABLE youtube_videos (
  id_video SERIAL PRIMARY KEY,
  titulo_video VARCHAR(255) NOT NULL,
  nome_canal VARCHAR(255) NOT NULL,
  catergoria VARCHAR(100),
  visualizacoes BIGINT,
  likes BIGINT,
  comentarios BIGINT,
  data_publicacao DATE,
  regiao VARCHAR(100)
  
);

CREATE TABLE correlacao (
  id_relacao SERIAL PRIMARY KEY,
  id_musica INTEGER REFERENCES spotify_musicas(id_musica),
  id_videos INTEGER REFERENCES youtube_videos(id_video),
  detalhe VARCHAR(255)
);