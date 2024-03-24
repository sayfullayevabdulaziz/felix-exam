from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.database import get_session
from src.public.unit.crud import (
    create_unit_crud,
    delete_unit,
    read_unit,
    read_units,
    update_unit_crud,
)
from src.public.unit.models import UnitCreate, UnitRead, UnitUpdate
from src.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("", response_model=UnitRead)
async def create_unit(unit: UnitCreate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.create_a_unit: {unit}")
    unit = create_unit_crud(unit=unit, db=db)
    return UnitRead(id=unit.id, name=unit.name)


@router.get("", response_model=list[UnitRead])
async def get_units(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    logger.info(f"{__name__}.get_units: triggered")
    return read_units(offset=offset, limit=limit, db=db)


@router.get("/{unit_id}", response_model=UnitRead)
async def get_unit(unit_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.get_a_unit.id: {unit_id}")
    return read_unit(unit_id=unit_id, db=db)


@router.patch("/{unit_id}", response_model=UnitRead)
async def update_unit(unit_id: int, unit: UnitUpdate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.update_a_Unit.id: {unit_id}")
    unit = update_unit_crud(unit_id=unit_id, unit=unit, db=db)
    return UnitRead(id=unit.id, name=unit.name)


@router.delete("/{unit_id}")
def delete_a_Unit(unit_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.delete_unit: {unit_id} triggered")
    return delete_unit(unit_id=unit_id, db=db)