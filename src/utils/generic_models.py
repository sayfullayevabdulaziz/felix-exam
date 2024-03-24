from decimal import Decimal
from sqlmodel import Field, SQLModel, Relationship


class ProductMaterialLink(SQLModel, table=True):
    product_id: int | None = Field(default=None, foreign_key="product.id", primary_key=True)
    material_id: int | None = Field(default=None, foreign_key="material.id", primary_key=True)
    quantity: Decimal = Field(default=0, max_digits=10, decimal_places=2)

    product: "Product" = Relationship(back_populates="material_links")
    material: "Material" = Relationship(back_populates="product_links")