from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from models import Medspa, Services
from repositories.services import ServicesRepository
import pytest

services_repository = ServicesRepository()

@pytest.fixture(autouse=True)
def setup_medspa(session: Session):
    medspa = Medspa(
        name="Test Medspa",
        address="123 Main St", 
        phone_number="123-456-7890",
        email_address="test@example.com"
    )
    session.add(medspa)
    session.commit()
    session.refresh(medspa)
    return medspa

def test_create_service(client: TestClient, session: Session, setup_medspa: Medspa):
    service_data = {
        "name": "Test Service",
        "description": "Test Description", 
        "price": 100.00,
        "duration": 30,
        "medspa_id": setup_medspa.id
    }

    response = client.post("/services/", json=service_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == service_data["name"]
    assert data["description"] == service_data["description"]
    assert data["price"] == "100.00"
    assert data["duration"] == service_data["duration"]

def test_create_service_with_invalid_medspa_id(client: TestClient):
    service_data = {
        "name": "Test Service",
        "description": "Test Description",
        "price": 100.00,
        "duration": 30,
        "medspa_id": 999
    }

    response = client.post("/services/", json=service_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Medspa not found"}

def test_get_service(client: TestClient, session: Session, setup_medspa: Medspa):
    service = Services(
        name="Test Service",
        description="Test Description",
        price=100.00,
        duration=30,
        medspa_id=setup_medspa.id
    )
    session.add(service)
    session.commit()
    session.refresh(service)

    response = client.get(f"/services/{service.id}")
    
    assert response.status_code == 200
    assert response.json()["name"] == service.name
    assert response.json()["description"] == service.description
    assert response.json()["price"] == "100.00"
    assert response.json()["duration"] == service.duration
    assert response.json()["medspa_id"] == setup_medspa.id

def test_get_services_filter_by_medspa_id(client: TestClient, session: Session, setup_medspa: Medspa):
    service = Services(
        name="Test Service",
        description="Test Description",
        price=100,
        duration=30,
        medspa_id=setup_medspa.id
    )
    services_repository.create(session, service)

    response = client.get(f"/services?medspa_id={setup_medspa.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == service.name   

    response = client.get(f"/services?medspa_id=999")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_update_service(client: TestClient, session: Session, setup_medspa: Medspa):
    service = Services(
        name="Test Service",
        description="Test Description",
        price=100,
        duration=30,
        medspa_id=setup_medspa.id
    )
    session.add(service)
    session.commit()
    session.refresh(service)

    update_data = {
        "name": "Updated Service",
    }

    response = client.patch(f"/services/{service.id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]
    assert response.json()["duration"] == service.duration


def test_delete_service(client: TestClient, session: Session, setup_medspa: Medspa):
    service = Services(
        name="Test Service",
        description="Test Description",
        price=100,
        duration=30,
        medspa_id=setup_medspa.id
    )
    session.add(service)
    session.commit()
    session.refresh(service)    

    response = client.delete(f"/services/{service.id}")
    assert response.status_code == 204

    # Verify that the service is deleted
    with pytest.raises(HTTPException) as exc_info:
        services_repository.get_by_id(session, service.id)

    assert exc_info.value.status_code == 404

    