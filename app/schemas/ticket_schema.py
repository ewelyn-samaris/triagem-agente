from pydantic import BaseModel, Field
from uuid import UUID

class TicketCreate(BaseModel):
    id_cliente: UUID = Field(..., description='ID único do cliente que abriu o ticket')
    texto_solicitacao: str = Field(..., min_length=10, max_length=120, description='Descrição detalhada da issue')