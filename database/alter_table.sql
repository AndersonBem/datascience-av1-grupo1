-- Spotify: padronizar duração
ALTER TABLE spotify_musicas
RENAME COLUMN duracao TO duracao_ms;
-- YouTube: padronizar canal com o CSV/código
ALTER TABLE youtube_videos
RENAME COLUMN nome_canal TO canal;
-- Correlações: corrigir nome da coluna
ALTER TABLE correlacoes
RENAME COLUMN valor_contratado TO valor_encontrado;
-- Correlações: adicionar popularidade/score do vídeo
ALTER TABLE correlacoes
ADD COLUMN popularidade_video NUMERIC(15,2);
ALTER TABLE correlacoes
ADD COLUMN nome_musica VARCHAR(255),
ADD COLUMN artista VARCHAR(255),
ADD COLUMN titulo_video VARCHAR(255),
ADD COLUMN canal VARCHAR(255);
ALTER TABLE correlacoes
RENAME COLUMN popularidade_spotify TO popularidade_musica;

ALTER TABLE correlacoes
RENAME COLUMN visualizacoes_youtube TO visualizacoes_video;

ALTER TABLE correlacoes
RENAME COLUMN nome_musica TO musica;

ALTER TABLE correlacoes
ADD COLUMN IF NOT EXISTS album VARCHAR(255);

ALTER TABLE correlacoes
ADD COLUMN IF NOT EXISTS data_lancamento_musica DATE;

ALTER TABLE correlacoes
ADD COLUMN IF NOT EXISTS data_lancamento_video DATE;