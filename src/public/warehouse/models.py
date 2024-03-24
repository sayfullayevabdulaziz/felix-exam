from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship
from src.public.material.models import Material


class WarehouseBase(SQLModel):
    material_id: int | None = Field(foreign_key="material.id")
    reaminder: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    price: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    
    

class Warehouse(WarehouseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    batch_identifier: str = Field(default_factory=lambda: f'BATCH-{datetime.now().strftime("%Y%m%d-%H%M%S")}')
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
    created_at: datetime | None = Field(default_factory=datetime.now)
    material: Material = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Warehouse.material_id==Material.id",
        }
    )

    @property
    def material_name(self) -> str:
        return self.material.name
    

class WarehouseCreate(WarehouseBase):
    pass


class WarehouseRead(SQLModel):
    id: int
    reaminder: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    price: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    batch_identifier: str
    material: str | None = Field(alias='material_name')


class WarehouseUpdate(WarehouseBase):
    reaminder: Decimal | None = None
    price: Decimal | None = None


class CheckMaterialsWarehouse(SQLModel):
    product_id: int
    quantity: int


class ResultMaterialsWarehouse(SQLModel):
    product_id: int
    quantity: int
    product_materials: list[WarehouseRead]