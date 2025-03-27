from sqlalchemy import delete
from sqlmodel import Session
from .base import BaseRepository
from models import AppointmentsServices

class AppointmentsServicesRepository(BaseRepository[AppointmentsServices]):
    def __init__(self):
        super().__init__(AppointmentsServices) 

    def delete_by_appointment_id(self, session: Session, appointment_id: int) -> None:
        query = delete(AppointmentsServices).where(AppointmentsServices.appointment_id == appointment_id)
        session.exec(query)
        session.commit()