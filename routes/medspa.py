from fastapi import APIRouter
from database import SessionDep
from models import Medspa
from repositories.medspa import MedspaRepository


router = APIRouter(
    prefix="/medspas",
    tags=["medspas"],
)

medspa_repository = MedspaRepository()

@router.get("/")
def read_medspas(session: SessionDep) -> list[Medspa]:
    medspas = medspa_repository.get_all(session)
    return medspas

@router.get("/{medspa_id}")
def read_medspa(medspa_id: int, session: SessionDep) -> Medspa:
    medspa = medspa_repository.get_by_id(session, medspa_id)
    return medspa

@router.post("/", status_code=201)
def create_medspa(medspa: Medspa, session: SessionDep) -> Medspa:
    item = medspa_repository.create(session, medspa)
    return item

@router.patch("/{medspa_id}")
def update_medspa(medspa_id: int, medspa: Medspa, session: SessionDep) -> Medspa:
    item = medspa_repository.update(session, medspa_id, medspa)
    return item

@router.delete("/{medspa_id}", status_code=204)
def delete_medspa(medspa_id: int, session: SessionDep) -> None:
    medspa_repository.delete(session, medspa_id)
    