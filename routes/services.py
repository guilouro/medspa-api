from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Field, SQLModel, Session, select
from database import SessionDep
from models import Services
from repositories.medspa import MedspaRepository
from repositories.services import ServicesRepository


router = APIRouter(
    prefix="/services",
    tags=["services"],
)

services_repository = ServicesRepository()
medspa_repository = MedspaRepository()

@router.get("/")
def read_services(session: SessionDep, medspa_id: int | None = None) -> list[Services]:
    filter = {"medspa_id": medspa_id} if medspa_id else {}
    services = services_repository.get_all(session, **filter)
    return services

@router.get("/{service_id}")
def read_service(service_id: int, session: SessionDep) -> Services:
    service = services_repository.get_by_id(session, service_id)
    return service

@router.post("/", status_code=201)
def create_service(service: Services, session: SessionDep) -> Services:
    service.medspa = medspa_repository.get_by_id(session, service.medspa_id)
    item = services_repository.create(session, service)
    return item

@router.patch("/{service_id}")
def update_service(service_id: int, service: Services, session: SessionDep) -> Services:
    item = services_repository.update(session, service_id, service)
    return item

@router.delete("/{service_id}", status_code=204)
def delete_service(service_id: int, session: SessionDep) -> None:
    services_repository.delete(session, service_id)
    