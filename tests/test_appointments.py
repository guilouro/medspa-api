from datetime import datetime
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from repositories.appoitments import AppointmentsRepository
from repositories.medspa import MedspaRepository
from repositories.services import ServicesRepository
from models import AppointmentStatus, Appointments, Medspa, Services
import pytest

medspa_repository = MedspaRepository()
services_repository = ServicesRepository()
appointments_repository = AppointmentsRepository()

@pytest.fixture(autouse=True)
def setup_medspa(session: Session):
    medspa = Medspa(
        name="Test Medspa",
        address="123 Main St", 
        phone_number="123-456-7890",
        email_address="test@example.com"
    )
    medspa_repository.create(session, medspa)
    return medspa

@pytest.fixture(autouse=True)
def setup_service(session: Session, setup_medspa: Medspa):
    service1 = Services(
        name="Test Service 1",
        description="Test Description 1", 
        price=100,
        duration=30,
        medspa_id=setup_medspa.id
    )
    
    service2 = Services(
        name="Test Service 2", 
        description="Test Description 2",
        price=200,
        duration=60,
        medspa_id=setup_medspa.id
    )
    
    services_repository.create(session, service1)
    services_repository.create(session, service2)
    return [service1, service2]

def test_get_appointments(client: TestClient, session: Session, setup_medspa: Medspa):

    start_time = datetime.now()
    appointment = appointments_repository.create(session, Appointments(
        medspa_id=setup_medspa.id,
        start_time=start_time,
        total_price=300,
        total_duration=90
    ))

    response = client.get(f"/appointments/{appointment.id}")
    assert response.status_code == 200
    assert response.json()["medspa_id"] == setup_medspa.id
    assert response.json()["start_time"] == start_time.isoformat()
    assert response.json()["total_price"] == "300.00"

def test_get_appointments_filter_by_status(client: TestClient, session: Session, setup_medspa: Medspa, setup_service: Services):
    appointment1 = Appointments(
        medspa_id=setup_medspa.id,
        start_time=datetime.now(),
        total_price=300,
        total_duration=90,
        status=AppointmentStatus.SCHEDULED
    )
    appointments_repository.create(session, appointment1)

    appointment2 = Appointments(
        medspa_id=setup_medspa.id,
        start_time=datetime.now(),
        total_price=300,
        total_duration=90,
        status=AppointmentStatus.CANCELLED
    )
    appointments_repository.create(session, appointment2)

    response = client.get(f"/appointments?status={AppointmentStatus.SCHEDULED.value}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == appointment1.id

    response = client.get(f"/appointments?status={AppointmentStatus.CANCELLED.value}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == appointment2.id

def test_create_appointment(client: TestClient, session: Session, setup_medspa: Medspa, setup_service: Services):
    appointment = {
        "medspa_id": setup_medspa.id,
        "services": [setup_service[0].id, setup_service[1].id]
    }

    response = client.post(f"/appointments", json=appointment)
    assert response.status_code == 201
    assert response.json()["medspa_id"] == setup_medspa.id
    assert response.json()["status"] == AppointmentStatus.SCHEDULED.value
    assert response.json()["total_price"] == "300.00"
    assert response.json()["total_duration"] == 90

def test_update_appointment_status(client: TestClient, session: Session, setup_medspa: Medspa, setup_service: Services):
    service = Services(
        name="Test Service 3",
        description="Test Description 3", 
        price=298,
        duration=45,
        medspa_id=setup_medspa.id
    )
    services_repository.create(session, service)

    appointment = Appointments(
        medspa_id=setup_medspa.id,
        start_time=datetime.now(),
        total_price=300,
        total_duration=90
    )
    appointments_repository.create(session, appointment)

    updated_appointment = {
        "status": "cancelled",
        "services": [setup_service[0].id, service.id]
    }

    response = client.patch(f"/appointments/{appointment.id}", json=updated_appointment)
    assert response.status_code == 200
    assert response.json()["medspa_id"] == setup_medspa.id
    assert response.json()["status"] == "cancelled"
    assert response.json()["total_price"] == "398.00"
    assert response.json()["total_duration"] == 75

def test_delete_appointment(client: TestClient, session: Session, setup_medspa: Medspa, setup_service: Services):
    appointment = Appointments(
        medspa_id=setup_medspa.id,
        start_time=datetime.now(),
        total_price=300,
        total_duration=90
    )
    appointments_repository.create(session, appointment)

    response = client.delete(f"/appointments/{appointment.id}")
    assert response.status_code == 204

    # Test that the appointment is deleted
    with pytest.raises(HTTPException) as exc_info:
        appointments_repository.get_by_id(session, appointment.id)

    assert exc_info.value.status_code == 404
