from decimal import Decimal
from fastapi import HTTPException, status
from sqlmodel import Session, select, and_


from src.public.product.crud import read_product
from src.public.material.crud import read_material
from src.public.warehouse.models import CheckMaterialsWarehouse, ResultMaterialsWarehouse, Warehouse, WarehouseCreate, WarehouseRead, WarehouseUpdate



def create_warehouse_crud(warehouse: WarehouseCreate, db: Session):
    read_material(material_id=warehouse.material_id, db=db)
    warehouse_to_db = Warehouse.model_validate(warehouse)
    db.add(warehouse_to_db)
    db.commit()
    db.refresh(warehouse_to_db)
    return warehouse_to_db


def read_warehouses(db: Session, offset: int = 0, limit: int = 20):
    warehouses = db.exec(select(Warehouse).offset(offset).limit(limit)).all()
    return warehouses


def read_warehouses_by_material_id(material_id: int, db: Session, offset: int = 0, limit: int = 20):
    warehouses = db.exec(
        select(Warehouse).
        filter(and_(Warehouse.material_id==material_id, Warehouse.reaminder!=0)).
        offset(offset).
        limit(limit)
    ).all()
    return warehouses


def read_warehouse(warehouse_id: int, db: Session):
    warehouse = db.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse not found with id: {warehouse_id}",
        )
    return warehouse


def update_warehouse_crud(warehouse_id: int, warehouse: WarehouseUpdate, db: Session):
    warehouse_to_update = db.get(Warehouse, warehouse_id)
    if not warehouse_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse not found with id: {warehouse_id}",
        )

    warehouse_data = warehouse.model_dump(exclude_unset=True)
    for key, value in warehouse_data.items():
        setattr(warehouse_to_update, key, value)

    db.add(warehouse_to_update)
    db.commit()
    db.refresh(warehouse_to_update)
    return warehouse_to_update


def delete_warehouse(warehouse_id: int, db: Session):
    warehouse = db.get(Warehouse, warehouse_id)
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse not found with id: {warehouse_id}",
        )

    db.delete(warehouse)
    db.commit()


def check_materials_from_warehouse_crud(check_materials: list[CheckMaterialsWarehouse], db: Session):
    booked_warehouses: list[str] = []
    result: list[ResultMaterialsWarehouse] = []
    for product_material in check_materials:
        product_materials: list = []
        
        product = read_product(product_id=product_material.product_id, db=db)
        all_needed_materials = list(map(lambda material: (material.material_id, Decimal(material.quantity*product_material.quantity)), product.material_links))
        
        for material_id, material_quantity in all_needed_materials:    
            for warehouse in read_warehouses_by_material_id(material_id=material_id, db=db):
                if warehouse.batch_identifier not in booked_warehouses:
                    if warehouse.reaminder <= material_quantity:
                        material_quantity -= warehouse.reaminder
                        booked_warehouses.append(warehouse.batch_identifier)
                        product_materials.append(
                            WarehouseRead(
                                id=warehouse.id, 
                                batch_identifier=warehouse.batch_identifier, 
                                reaminder=warehouse.reaminder, 
                                price=warehouse.price, 
                                material=warehouse.material_name
                            )
                        )

                    else:
                        warehouse.reaminder -= material_quantity
                        
                        product_materials.append(
                            WarehouseRead(
                                id=warehouse.id, 
                                batch_identifier=warehouse.batch_identifier, 
                                reaminder=material_quantity, 
                                price=warehouse.price, 
                                material=warehouse.material_name
                            )
                        )
                        material_quantity = 0
                    
            
        result.append(ResultMaterialsWarehouse(
            product_id=product_material.product_id,
            quantity=product_material.quantity,
            product_materials=product_materials
        ))
    return result
