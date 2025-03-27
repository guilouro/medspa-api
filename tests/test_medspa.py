from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from repositories.medspa import MedspaRepository
from models import Medspa

medspa_repository = MedspaRepository()


def test_create_medspa(client: TestClient):
    medspa_data = {
        "name": "Test Medspa",
        "address": "123 Main St",
        "phone_number": "123-456-7890",
        "email_address": "test@example.com",
    }

    response = client.post("/medspas/", json=medspa_data)

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "Test Medspa",
        "address": "123 Main St",
        "phone_number": "123-456-7890",
        "email_address": "test@example.com",
        "created_at": response.json()["created_at"],
        "updated_at": response.json()["updated_at"],
    }


def test_get_medspa(client: TestClient, session: Session):
    medspa = Medspa(
        name="Test Medspa",
        address="123 Main St",
        phone_number="123-456-7890",
        email_address="test@example.com",
    )

    medspa_repository.create(session, medspa)

    response = client.get(f"/medspas/{medspa.id}")
    assert response.status_code == 200

    assert response.json()["name"] == medspa.name
    assert response.json()["address"] == medspa.address
    assert response.json()["phone_number"] == medspa.phone_number
    assert response.json()["email_address"] == medspa.email_address


def test_update_medspa(client: TestClient, session: Session):
    medspa = Medspa(
        name="Test Medspa",
        address="123 Main St",
        phone_number="123-456-7890",
        email_address="test@example.com",
    )

    medspa_repository.create(session, medspa)

    updated_medspa_data = {
        "name": "Updated Medspa",
        "email_address": "updated@example.com",
    }

    response = client.patch(f"/medspas/{medspa.id}", json=updated_medspa_data)
    assert response.status_code == 200

    assert response.json()["name"] == updated_medspa_data["name"]
    assert response.json()["email_address"] == updated_medspa_data["email_address"]
    assert response.json()["address"] == medspa.address
    assert response.json()["phone_number"] == medspa.phone_number


def test_delete_medspa(client: TestClient, session: Session):
    medspa = Medspa(
        name="Test Medspa",
        address="123 Main St",
        phone_number="123-456-7890",
        email_address="test@example.com",
    )

    medspa_repository.create(session, medspa)

    response = client.delete(f"/medspas/{medspa.id}")
    assert response.status_code == 204

    # Verify that the medspa is deleted
    with pytest.raises(HTTPException) as exc_info:
        medspa_repository.get_by_id(session, medspa.id)

    assert exc_info.value.status_code == 404
