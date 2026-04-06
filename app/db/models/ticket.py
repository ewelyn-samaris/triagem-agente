import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from app.db.database import Base
from app.db.categoria_enum import Categoria
from app.db.urgencia_enum import Urgencia


class Ticket(Base):
    __tablename__ = 'tickets'
 
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_cliente = Column(String, nullable=False, index=True)
    texto_solicitacao = Column(String, nullable=False)
    categoria = Column(SQLEnum(Categoria), nullable=False)
    urgencia = Column(SQLEnum(Urgencia), nullable=False)
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))