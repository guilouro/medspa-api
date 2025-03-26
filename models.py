import datetime
from decimal import Decimal
from typing import List
from sqlmodel import Field, Relationship, SQLModel

class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    created_at: datetime.datetime = Field(default=datetime.datetime.now())
    updated_at: datetime.datetime = Field(default=datetime.datetime.now())


class Medspa(Base, table=True):
    name: str
    address: str
    phone_number: str
    email_address: str

    services: List["Services"] = Relationship(back_populates="medspa")


class Services(Base, table=True):
    medspa_id: int = Field(foreign_key="medspa.id")
    name: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
    duration: int

    medspa: Medspa = Relationship(back_populates="services")
