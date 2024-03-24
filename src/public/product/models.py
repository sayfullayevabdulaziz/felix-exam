from datetime import datetime
from decimal import Decimal
from typing import List
from sqlmodel import Field, SQLModel, Relationship
from src.utils.generic_models import ProductMaterialLink


class ProductAddMaterials(SQLModel):
    material_id: int
    quantity: Decimal = Field(default=0, max_digits=10, decimal_places=2)


class ProductBase(SQLModel):
    name: str = Field(index=True)
    code: str = Field(index=True)


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
    created_at: datetime | None = Field(default_factory=datetime.now)

    material_links: List[ProductMaterialLink] = Relationship(back_populates="product")
    

class ProductCreate(ProductBase):
    materials: List[ProductAddMaterials]


class ProductRead(ProductBase):
    id: int
    materials: List[ProductAddMaterials]


class ProductUpdate(ProductBase):
    name: str | None = None
    code: str | None = None
