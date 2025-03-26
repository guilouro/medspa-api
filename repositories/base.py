from typing import TypeVar, Generic, Type
from fastapi import HTTPException
from sqlmodel import SQLModel, select, Session

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_all(self, session: Session) -> list[ModelType]:
        query = select(self.model)
        return session.exec(query).all()
    
    def get_by_id(self, session: Session, id: int) -> ModelType:
        query = select(self.model).where(self.model.id == id)
        item = session.exec(query).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return item
    
    def create(self, session: Session, item: ModelType) -> ModelType:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item

    def update(self, session: Session, id: int, item: ModelType) -> ModelType:
        current_item = self.get_by_id(session, id)
        update_data = item.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(current_item, key, value)

        session.add(current_item)
        session.commit()
        session.refresh(current_item)
        return current_item 
    
    def delete(self, session: Session, id: int) -> None:
        item = self.get_by_id(session, id)
        session.delete(item)
        session.commit()