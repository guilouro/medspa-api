import datetime
from decimal import Decimal
from enum import Enum
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
    appointments: List["Appointments"] = Relationship(back_populates="medspa")


class Services(Base, table=True):
    medspa_id: int = Field(foreign_key="medspa.id")
    name: str
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
    duration: int

    medspa: Medspa = Relationship(back_populates="services")
    appointments: List["AppointmentsServices"] = Relationship(back_populates="service")

class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AppointmentCreate(SQLModel):
    medspa_id: int
    services: List[int]

class AppointmentUpdate(SQLModel):
    medspa_id: int | None = None
    status: AppointmentStatus | None = None 
    services: List[int] | None = None

class Appointments(Base, table=True):
    medspa_id: int = Field(foreign_key="medspa.id")
    start_time: datetime.datetime
    total_price: Decimal = Field(max_digits=10, decimal_places=2)
    total_duration: int
    status: AppointmentStatus = Field(default=AppointmentStatus.SCHEDULED)

    medspa: Medspa = Relationship(back_populates="appointments")
    services: List["AppointmentsServices"] = Relationship(back_populates="appointment")

class AppointmentsServices(Base, table=True):
    __tablename__ = "appointments_services"

    appointment_id: int = Field(foreign_key="appointments.id")
    service_id: int = Field(foreign_key="services.id")

    appointment: List["Appointments"] = Relationship(back_populates="services")
    service: List["Services"] = Relationship(back_populates="appointments")