from .base import BaseRepository
from models import Services


class ServicesRepository(BaseRepository[Services]):
    def __init__(self):
        super().__init__(Services)
