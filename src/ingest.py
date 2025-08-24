import pandas as pd
from sqlalchemy import create_engine

# Caminho do arquivo CSV
csv_path = './data/IOT-temp.csv'

# Lê o CSV original
df = pd.read_csv(csv_path)

# Renomeia colunas para padronizar
df.columns = ['id', 'room_id', 'data_registro', 'temperatura', 'direcao']

# Cria a coluna 'modelo' com os 6 números após "log_"
df['modelo'] = df['id'].str.extract(r'log_(\d{6})')

# Remove linhas com extração falha
df = df.dropna(subset=['modelo'])

# Conecta ao banco de dados PostgreSQL
engine = create_engine('postgresql://postgres:71216@localhost:5432/iot')

# Cria DataFrame com colunas já no padrão da tabela 'temperaturas'
df_final = df[['modelo', 'data_registro', 'temperatura', 'direcao']]

# Insere no banco substituindo se já existir
try:
    df_final.to_sql('temperaturas', engine, if_exists='replace', index=False)
    print("✅ Dados inseridos com sucesso!")
except Exception as e:
    print("❌ Erro ao inserir dados:", e)
