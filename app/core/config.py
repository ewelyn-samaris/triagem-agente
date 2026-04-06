from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    '''
    Centraliza todas as configurações do sistema, validando a presença e os tipos
    de dados no momento em que a aplicação é criada
    '''
    
    DATABASE_URL:str
    GEMINI_API_KEY: str
    MODEL_NAME: str = "gemini-1.5-flash"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings() -> Settings:
    '''
    Singleton via cache. env só será lido 1x durante vida útil da aplicação
    '''
    return Settings()
