# 📡 Pipeline de Dados com IoT, PostgreSQL, Docker e Streamlit

Este projeto desenvolve um pipeline completo de ingestão, armazenamento e visualização de dados de sensores IoT utilizando Python, PostgreSQL, Docker e Streamlit. Ele processa dados reais de temperatura registrados por dispositivos e gera um dashboard interativo.

---

## 🗂️ Estrutura do Projeto

```bash
📦 projeto-iot
├── assets/
│   ├── pdf
│       └── kaio-santana-71216.pdf
│   ├── prints
│       └── 001.png
│       └── 002.png
│       └── 003.png
│       └── 00.png
├── data/
│   └── IOT-temp.csv
├── database/
│   └── init.sql
├── src/
│   ├── app.py
│   └── ingest.py
├── .env
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔧 Tecnologias Utilizadas

- Python 3.11
- Streamlit
- PostgreSQL 16
- Docker e Docker Compose
- SQLAlchemy
- Pandas
- psycopg2
- dotenv

---

## 📦 Instalação das Bibliotecas Python

Execute o comando abaixo para instalar as dependências do projeto:

```bash
pip install -r requirements.txt
```

Conteúdo do `requirements.txt`:

```txt
streamlit
pandas
sqlalchemy
psycopg2
python-dotenv
```

---

## 🐘 Banco de Dados PostgreSQL com Docker

Para criar o banco PostgreSQL com Docker, utilize o seguinte `docker-compose.yml`:

```yaml
version: '3.1'

services:
  db:
    image: postgres:16
    container_name: iot-db
    environment:
      POSTGRES_DB: iot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 71216
    ports:
      - "5432:5432"
    volumes:
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
```

---

## 🧱 Script de Criação da Tabela e Views (init.sql)

```sql
-- Criação da tabela
CREATE TABLE IF NOT EXISTS temperaturas (
    modelo VARCHAR(10),
    data_registro TIMESTAMP,
    temperatura INT,
    direcao VARCHAR(10)
);

-- View 1: Temperaturas por modelo
CREATE OR REPLACE VIEW vw_temperaturas_por_modelo AS
SELECT modelo, data_registro, temperatura, direcao
FROM temperaturas;

-- View 2: Média geral
CREATE OR REPLACE VIEW vw_media_temperatura_por_modelo AS
SELECT 'Média de temperaturas' AS modelo, ROUND(AVG(temperatura)) AS media_de_temperaturas
FROM temperaturas;

-- View 3: Temperatura mínima
CREATE OR REPLACE VIEW vw_min_temp_por_modelo AS
SELECT modelo, MIN(temperatura) AS menor_temperatura
FROM temperaturas
GROUP BY modelo
ORDER BY menor_temperatura ASC
LIMIT 1;

-- View 4: Temperatura máxima
CREATE OR REPLACE VIEW vw_max_temp_por_modelo AS
SELECT modelo, MAX(temperatura) AS maior_temperatura
FROM temperaturas
GROUP BY modelo
ORDER BY maior_temperatura DESC
LIMIT 1;
```

---

## 🚀 Pipeline de Ingestão de Dados (ingest.py)

```python
import pandas as pd
from sqlalchemy import create_engine

csv_path = './data/IOT-temp.csv'
df = pd.read_csv(csv_path)

df.columns = ['id', 'room_id', 'noted_date', 'temp', 'local']
df['modelo'] = df['id'].str.extract(r'log_(\d{6})')
df = df.dropna(subset=['modelo'])

df['noted_date'] = pd.to_datetime(df['noted_date'], format="%d-%m-%Y %H:%M")
df = df[['modelo', 'noted_date', 'temp', 'local']]
df.columns = ['modelo', 'data_registro', 'temperatura', 'direcao']

db_url = 'postgresql://postgres:71216@localhost:5432/iot'
engine = create_engine(db_url)

try:
    df.to_sql('temperaturas', engine, if_exists='replace', index=False)
    print("✅ Dados inseridos com sucesso!")
except Exception as e:
    print("❌ Erro ao inserir dados:", e)
```

---

## 📊 Dashboard Interativo com Streamlit

Arquivo: `src/app.py`

```python
import streamlit as st
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

def carregar_view(nome_view):
    conn = conectar()
    df = pd.read_sql(f"SELECT * FROM {nome_view};", conn)
    conn.close()
    return df

st.set_page_config(page_title="Dashboard IoT", layout="wide")
st.title("📊 Dashboard de Temperaturas IoT")

st.header("📝 Temperaturas por Modelo")
st.dataframe(carregar_view("vw_temperaturas_por_modelo"))

st.header("📉 Média Geral das Temperaturas")
st.dataframe(carregar_view("vw_media_temperatura_por_modelo"))

st.header("❄️ Temperatura Mínima Registrada")
st.dataframe(carregar_view("vw_min_temp_por_modelo"))

st.header("🔥 Temperatura Máxima Registrada")
st.dataframe(carregar_view("vw_max_temp_por_modelo"))
```

---

## 📷 Prints do Projeto

| Etapa | Descrição | Imagem |
|-------|-----------|--------|
| 1     | Docker rodando com PostgreSQL | ![docker](./assets/prints/001.png) |
| 2     | Inserção dos dados | ![ingest](./assets/prints/002.png) |
| 3     | Views criadas | ![views](./assets/prints/003.png) |
| 4     | Dashboard final | ![dashboard](./assets/prints/004.png) |

---

## ⚙️ Como Executar o Projeto

```bash
# 1. Clonar o repositório
git clone https://github.com/Kaio-with-K/Dashboard_IOT-Kaio_Santana-71216.git

# 2. Ativar o venv no terminal
source venv/bin/activate

# 3. Subir o banco PostgreSQL com Docker
docker-compose up -d

# 4. Instalar as dependências
pip install -r requirements.txt

# 5. Executar o script de ingestão
python src/ingest.py

# 6. Rodar a aplicação Streamlit
streamlit run src/app.py
```

---

## 💡 Justificativas Técnicas

- **Docker:** garante ambiente isolado e reprodutível.
- **PostgreSQL:** banco relacional robusto para armazenar e consultar dados estruturados.
- **Views SQL:** facilitam o consumo de dados pelo dashboard sem complexidade no código Python.
- **Streamlit:** permite criar dashboards interativos com extrema agilidade e facilidade de uso.
- **Python:** linguagem ideal para manipulação de dados e integração com bancos de dados.

---

## 👨‍💻 Autor

Desenvolvido por **Kaio Santana**  
💼 Técnico em TI • Professor • Desenvolvedor • Designer

🔗[LinkedIn](https://www.linkedin.com/in/kaiojsantana/)
> 💡 *Dica: clique com o botão direito e selecione "Abrir em nova aba"*

---

## 📹 Vídeo no Youtube
🔗 [Clique aqui para assistir ao vídeo](https://www.youtube.com/watch?v=YtkB1NCOL-U)  
> 💡 *Dica: clique com o botão direito e selecione "Abrir em nova aba"*
