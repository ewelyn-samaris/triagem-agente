from app.core.config import get_settings
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    logger.critical('DATABASE_URL não foi definida nas variáveis de ambiente. O sistema não pode iniciar.')
    sys.exit(1)

try:
    engine=create_engine(DATABASE_URL)
    logger.info("Engine do banco de dados configurado com sucesso!")
except Exception as e:
    logger.error("Falha ao criar o engine do banco de dados: {e}")
    sys.exit(1)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    '''
    Gera uma sessão do banco de dados por requisição da API.
    Garante que a requisição será fechada após o uso, evitando vazamento de memória.
    '''

    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()

