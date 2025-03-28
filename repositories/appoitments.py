from datetime import datetime
from sqlmodel import Session, select
from .base import BaseRepository
from models import Appointments


class AppointmentsRepository(BaseRepository[Appointments]):
    def __init__(self):
        super().__init__(Appointments)

    def filter_date_query(self, date: datetime.date):
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())

        query = select(self.model).filter(
            self.model.start_time.between(start_datetime, end_datetime)
        )

        return query

    def get_all(self, session: Session, **filters) -> list[Appointments]:
        query = select(self.model)

        if filters:
            for key, value in filters.items():
                if key == "start_date":
                    query = self.filter_date_query(value)
                else:
                    query = query.where(getattr(self.model, key) == value)

        return session.exec(query).all()
