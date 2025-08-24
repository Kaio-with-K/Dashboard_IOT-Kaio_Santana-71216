from sqlalchemy import create_engine

try:
    engine = create_engine('postgresql://postgres:71216@localhost:5432/iot')
    with engine.connect() as conn:
        print("✅ Conexão com o banco estabelecida com sucesso!")
except Exception as e:
    print("❌ Erro de conexão:", e)
