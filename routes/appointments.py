import datetime
from fastapi import APIRouter
from database import SessionDep
from models import AppointmentStatus, AppointmentUpdate, Appointments, AppointmentsServices, AppointmentCreate
from repositories.services import ServicesRepository
from repositories.appoitments import AppointmentsRepository
from repositories.appoitments_services import AppointmentsServicesRepository
from repositories.medspa import MedspaRepository

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)

appointments_repository = AppointmentsRepository()
medspa_repository = MedspaRepository()
services_repository = ServicesRepository()
appointments_services_repository = AppointmentsServicesRepository()

@router.get("/")
def get_appointments(session: SessionDep, status: AppointmentStatus | None = None, start_date: datetime.date | None = None) -> list[Appointments]:
    filter = {"status": status} if status else {}

    appointments = appointments_repository.get_all(session, **filter)
    return appointments

@router.get("/{appointment_id}")
def get_appointment(appointment_id: int, session: SessionDep) -> dict:
    appointment = appointments_repository.get_by_id(session, appointment_id)
    
    # Get all appointment-service relationships for this appointment
    appointment_services = appointments_services_repository.get_all(session, appointment_id=appointment_id)
    
    # Get all services using the service IDs from the relationships
    service_ids = [aps.service_id for aps in appointment_services]
    services = services_repository.get_by_ids(session, service_ids)
    
    # Convert appointment to dict and exclude SQLModel metadata
    response = appointment.model_dump(exclude={"services"})
    response["services"] = [service.model_dump() for service in services]
    
    return response

@router.post("/", status_code=201)
def create_appointment(booking: AppointmentCreate, session: SessionDep) -> Appointments:
    medspa = medspa_repository.get_by_id(session, booking.medspa_id)
    services = services_repository.get_by_ids(session, booking.services)

    # Filter services to only include those belonging to the selected medspa
    services = [service for service in services if service.medspa_id == medspa.id]
    
    appointment = Appointments(
        medspa_id=medspa.id,
        start_time=datetime.datetime.now(),
        total_price=sum(service.price for service in services),
        total_duration=sum(service.duration for service in services),
        status=AppointmentStatus.SCHEDULED
    )

    appointments_repository.create_and_flush(session, appointment)

    for service in services:
        appointments_services = AppointmentsServices(
            appointment_id=appointment.id,
            service_id=service.id
        )
        appointments_services_repository.create(session, appointments_services)


    session.refresh(appointment)
    return appointment

@router.patch("/{appointment_id}")
def update_appointment(appointment_id: int, booking: AppointmentUpdate, session: SessionDep) -> Appointments:
    appointment = appointments_repository.get_by_id(session, appointment_id)
    
    if booking.medspa_id:
        appointment.medspa_id = booking.medspa_id

    if booking.status:
        appointment.status = booking.status

    if booking.services:
        services = services_repository.get_by_ids(session, booking.services)
        
        appointment.total_price = sum(service.price for service in services)
        appointment.total_duration = sum(service.duration for service in services)

        # Delete existing appointment-service relationships before creating new ones
        # This ensures we don't have orphaned or duplicate relationships when updating services
        appointments_services_repository.delete_by_appointment_id(session, appointment_id)
        for service in services:
            appointments_services = AppointmentsServices(
                appointment_id=appointment_id,
                service_id=service.id
            )
            appointments_services_repository.create(session, appointments_services)

    appointments_repository.update(session, appointment_id, appointment)
    return appointment

@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, session: SessionDep) -> None:
    appointments_repository.delete(session, appointment_id)