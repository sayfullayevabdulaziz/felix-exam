from fastapi import HTTPException, status
from sqlmodel import Session, select


from src.public.unit.models import Unit, UnitCreate, UnitUpdate


def create_unit_crud(unit: UnitCreate, db: Session):
    unit_to_db = Unit.model_validate(unit)
    db.add(unit_to_db)
    db.commit()
    db.refresh(unit_to_db)
    return unit_to_db


def read_units(db: Session, offset: int = 0, limit: int = 20, ):
    units = db.exec(select(Unit).offset(offset).limit(limit)).all()
    return units


def read_unit(unit_id: int, db: Session):
    unit = db.get(Unit, unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unit not found with id: {unit_id}",
        )
    return unit


def update_unit_crud(unit_id: int, unit: UnitUpdate, db: Session):
    unit_to_update = db.get(Unit, unit_id)
    if not unit_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unit not found with id: {unit_id}",
        )

    unit_data = unit.model_dump(exclude_unset=True)
    for key, value in unit_data.items():
        setattr(unit_to_update, key, value)

    db.add(unit_to_update)
    db.commit()
    db.refresh(unit_to_update)
    return unit_to_update


def delete_unit(unit_id: int, db: Session):
    unit = db.get(Unit, unit_id)
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unit not found with id: {unit_id}",
        )

    db.delete(unit)
    db.commit()