from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.database import get_session
from src.public.warehouse.crud import (
    check_materials_from_warehouse_crud,
    create_warehouse_crud,
    delete_warehouse,
    read_warehouse,
    read_warehouses,
    update_warehouse_crud,
)
from src.public.warehouse.models import CheckMaterialsWarehouse, WarehouseCreate, WarehouseRead, WarehouseUpdate
from src.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("", response_model=WarehouseRead)
async def create_warehouse(warehouse: WarehouseCreate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.create_a_warehouse: {warehouse}")
    warehouse = create_warehouse_crud(warehouse=warehouse, db=db)
    return WarehouseRead(
        id=warehouse.id, 
        batch_identifier=warehouse.batch_identifier, 
        reaminder=warehouse.reaminder, 
        price=warehouse.price, 
        material=warehouse.material_name
        )


@router.get("", response_model=list[WarehouseRead])
async def get_warehouses(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    logger.info(f"{__name__}.get_warehouses: triggered")
    warehouses = read_warehouses(offset=offset, limit=limit, db=db)
    return [WarehouseRead(
        id=warehouse.id, 
        batch_identifier=warehouse.batch_identifier, 
        reaminder=warehouse.reaminder, 
        price=warehouse.price, 
        material=warehouse.material_name
        ) for warehouse in warehouses]


@router.get("/{warehouse_id}", response_model=WarehouseRead)
async def get_warehouse(warehouse_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.get_a_warehouse.id: {warehouse_id}")
    warehouse = read_warehouse(warehouse_id=warehouse_id, db=db)
    return WarehouseRead(
        id=warehouse.id, 
        batch_identifier=warehouse.batch_identifier, 
        reaminder=warehouse.reaminder, 
        price=warehouse.price, 
        material=warehouse.material_name
        )


@router.post("/check-materials", status_code=200)
async def check_materials_from_warehouse(check_materials: list[CheckMaterialsWarehouse], db: Session = Depends(get_session)):
    logger.info(f"{__name__}.get_a_warehouse: {check_materials}")
    warehouse = check_materials_from_warehouse_crud(check_materials=check_materials, db=db)
    
    return warehouse
    # return WarehouseRead(
    #     id=warehouse.id, 
    #     batch_identifier=warehouse.batch_identifier, 
    #     reaminder=warehouse.reaminder, 
    #     price=warehouse.price, 
    #     material=warehouse.material_name
    #     )


@router.patch("/{warehouse_id}", response_model=WarehouseRead)
async def update_warehouse(warehouse_id: int, warehouse: WarehouseUpdate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.update_a_warehouse.id: {warehouse_id}")
    warehouse = update_warehouse_crud(warehouse_id=warehouse_id, warehouse=warehouse, db=db)
    return  WarehouseRead(
        id=warehouse.id, 
        batch_identifier=warehouse.batch_identifier, 
        reaminder=warehouse.reaminder, 
        price=warehouse.price, 
        material=warehouse.material_name
        )


@router.delete("/{warehouse_id}")
def delete_a_warehouse(warehouse_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.delete_warehouse: {warehouse_id} triggered")
    return delete_warehouse(warehouse_id=warehouse_id, db=db)