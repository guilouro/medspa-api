from .base import BaseRepository
from models import Medspa


class MedspaRepository(BaseRepository[Medspa]):
    def __init__(self):
        super().__init__(Medspa)
