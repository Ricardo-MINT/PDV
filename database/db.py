"""
Configuração do banco de dados SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Base para os modelos
Base = declarative_base()

# Caminho do banco de dados
# O dirname duplo garante que o db fique na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'pdv.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

# Engine e sessão
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    # IMPORTANTE: Importar os modelos aqui para que o SQLAlchemy os reconheça
    from models.produto import Produto
    from models.venda import Venda
    
    Base.metadata.create_all(bind=engine)
    
def get_db():
    """Retorna uma sessão do banco de dados (Gerenciador de Contexto)"""
    db = SessionLocal()
    try:
        return db
    finally:
        # Usamos finally para garantir que, se algo der errado 
        # após pegar a sessão, ela não fique aberta.
        db.close()