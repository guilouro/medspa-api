from sqlmodel import Session, select
from .base import BaseRepository
from models import Appointments

class AppointmentsRepository(BaseRepository[Appointments]):
    def __init__(self):
        super().__init__(Appointments) 

