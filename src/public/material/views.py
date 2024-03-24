from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.database import get_session
from src.public.material.crud import (
    create_material_crud,
    delete_material,
    read_material,
    read_materials,
    update_material_crud,
)
from src.public.material.models import MaterialCreate, MaterialRead, MaterialUpdate
from src.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("", response_model=MaterialRead)
async def create_material(material: MaterialCreate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.create_a_material: {material}")
    material = create_material_crud(material=material, db=db)
    return MaterialRead(id=material.id, name=material.name, unit=material.unit_name)


@router.get("", response_model=list[MaterialRead])
async def get_materials(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    logger.info(f"{__name__}.get_materials: triggered")
    materials = read_materials(offset=offset, limit=limit, db=db)
    return [MaterialRead(id=material.id, name=material.name, unit=material.unit_name) for material in materials]


@router.get("/{material_id}", response_model=MaterialRead)
async def get_material(material_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.get_a_material.id: {material_id}")
    material = read_material(material_id=material_id, db=db)
    return MaterialRead(id=material.id, name=material.name, unit=material.unit_name)


@router.patch("/{material_id}", response_model=MaterialRead)
async def update_material(material_id: int, material: MaterialUpdate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.update_a_material.id: {material_id}")
    material = update_material_crud(material_id=material_id, material=material, db=db)
    return MaterialRead(id=material.id, name=material.name, unit=material.unit_name)


@router.delete("/{material_id}")
def delete_a_material(material_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.delete_material: {material_id} triggered")
    return delete_material(material_id=material_id, db=db)