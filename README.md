# Projeto Data Science — Spotify & YouTube Analytics

## Integrantes

* Anderson Bem
* Wendell Barboza
* Laís Nayara
* Lucas Mendes
* Wendell Brasiliano

---

# Sobre o Projeto

Este projeto tem como objetivo realizar um processo completo de ETL (Extract, Transform, Load) utilizando dados do Spotify e YouTube.

Os dados são extraídos das APIs, tratados e correlacionados para gerar análises sobre:

* músicas populares;
* vídeos populares;
* engajamento;
* tendências;
* regiões;
* relações entre Spotify e YouTube.

Após o processamento, os dados são armazenados em um banco PostgreSQL e visualizados em um dashboard interativo desenvolvido com Streamlit.

---

# Tecnologias Utilizadas

## Linguagem

* Python

## Banco de Dados

* PostgreSQL

## Bibliotecas

* pandas
* sqlalchemy
* python-dotenv
* streamlit
* plotly
* psycopg2
* requests

---

# Estrutura do Projeto

```txt
PROJETO_DATASCIENCE/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   ├── schema.sql
│   └── alter_table.sql
│
├── extract/
│   ├── spotify_extract.py
│   └── youtube_extract.py
│
├── load/
│   └── load_to_database.py
│
├── transform/
│   ├── transform_spotify.py
│   ├── transform_youtube.py
│   └── correlation.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Funcionamento do Projeto

## 1. Extract

A etapa de extração realiza a coleta de dados das APIs.

### Spotify

Dados extraídos:

* nome da música;
* artista;
* álbum;
* popularidade;
* duração;
* gênero;
* data de lançamento;
* playlist.

### YouTube

Dados extraídos:

* título do vídeo;
* canal;
* categoria;
* visualizações;
* likes;
* comentários;
* região;
* data de publicação.

Os arquivos são salvos em:

```txt
/data/raw
```

---

## 2. Transform

A etapa de transformação realiza:

* limpeza dos dados;
* padronização;
* remoção de duplicados;
* tratamento de datas;
* cálculo de engajamento;
* organização dos datasets.

Os arquivos tratados são salvos em:

```txt
/data/processed
```

Arquivos gerados:

```txt
spotify_clean.csv
youtube_clean.csv
```

---

## 3. Correlation

A etapa de correlação cruza dados entre Spotify e YouTube.

Objetivos:

* identificar músicas populares que aparecem em vídeos populares;
* identificar artistas populares nas duas plataformas;
* relacionar popularidade Spotify com visualizações YouTube.

A correlação gera:

```txt
correlation.csv
```

---

## 4. Load

A etapa de carga envia os dados tratados para o PostgreSQL.

Tabelas utilizadas:

* spotify_musicas
* youtube_videos
* correlacoes

Antes da carga, as tabelas são limpas automaticamente para evitar duplicação.

---

## 5. Dashboard

O dashboard foi desenvolvido utilizando Streamlit.

Principais funcionalidades:

* Top músicas por popularidade;
* Top vídeos por visualizações;
* gráfico de dispersão entre Spotify e YouTube;
* análise regional;
* tabelas interativas;
* filtros por:

  * artista;
  * canal;
  * gênero;
  * região;
  * período;
  * engajamento.

---

# Banco de Dados

## Criação das tabelas

Execute:

```sql
schema.sql
```

## Ajustes adicionais

Execute:

```sql
alter_table.sql
```

---

# Configuração do Ambiente

## 1. Criar ambiente virtual

```bash
python -m venv venv
```

## 2. Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Arquivo .env

Criar arquivo:

```txt
.env
```

Exemplo:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_banco
SPOTIFY_CLIENT_ID=SEU_CLIENT_ID
SPOTIFY_CLIENT_SECRET=SEU_CLIENT_SECRET
YOUTUBE_API_KEY=SUA_API_KEY
```

---

# Como Executar o Projeto

## 1. Executar extração

```bash
python extract/spotify_extract.py
python extract/youtube_extract.py
```

---

## 2. Executar transformação

```bash
python transform/transform_spotify.py
python transform/transform_youtube.py
```

---

## 3. Executar correlação

```bash
python transform/correlation.py
```

---

## 4. Executar carga no banco

```bash
python load/load_to_database.py
```

---

## 5. Executar dashboard

```bash
streamlit run dashboard/app.py
```

---

# Métricas Utilizadas

## Spotify

* top_musicas_por_popularidade
* artistas_mais_frequentes
* duracao_media_das_musicas
* generos_mais_populares

## YouTube

* videos_mais_visualizados
* videos_com_maior_engajamento
* categorias_mais_populares
* engajamento_por_regiao

## Correlação

* musicas_populares_no_spotify_que_tambem_aparecem_no_youtube
* artistas_populares_nas_duas_plataformas
* relacao_entre_popularidade_spotify_e_views_youtube

---

# Principais Aprendizados

Durante o desenvolvimento do projeto foram trabalhados conceitos como:

* ETL;
* APIs;
* manipulação de dados;
* limpeza e transformação de datasets;
* banco de dados relacional;
* visualização de dados;
* dashboards interativos;
* integração entre plataformas.

---

# Observações

* O projeto foi desenvolvido para fins acadêmicos.
* Os dados podem variar dependendo da API.
* Algumas correlações podem variar conforme tendências atuais.

---



