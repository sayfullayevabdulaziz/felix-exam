from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

from src.public.unit.models import Unit, UnitMaterial
# from src.public.product.models import Product
from src.utils.generic_models import ProductMaterialLink

class MaterialBase(SQLModel):
    name: str = Field(index=True)
    unit_id: int | None = Field(foreign_key="unit.id")

class Material(MaterialBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    unit: Unit = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Material.unit_id==Unit.id",
        }
    )

    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
    created_at: datetime | None = Field(default_factory=datetime.now)

    product_links: list[ProductMaterialLink] = Relationship(back_populates="material")

    @property
    def unit_name(self):
        return self.unit.name


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(SQLModel):
    id: int
    name: str
    unit: str = Field(alias='unit_name')


class MaterialUpdate(MaterialBase):
    name: str | None = None