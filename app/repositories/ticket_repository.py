from sqlalchemy.orm import Session
from app.db.models.ticket import Ticket

class TicketRepository:

    def __init__(self, db_session: Session):
        self.db = db_session

    def criar(self, ticket: Ticket) -> Ticket:
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
    
    def buscar_por_id(self, ticket_id: str) -> Ticket | None:
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    def listar(self, limite: int = 100, offset: int = 0) -> list[Ticket]:
        return self.db.query(Ticket).offset(offset).limit(limite).all()
    
    def atualizar(self, ticket: Ticket) -> Ticket:
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
    
    def deletar(self, ticket_id: str) -> bool:
        ticket = self.buscar_por_id(ticket_id)

        if not ticket: 
            return False

        self.db.delete(ticket)
        self.db.commit()
        return True