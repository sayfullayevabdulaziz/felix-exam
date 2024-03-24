from datetime import datetime
from sqlmodel import Field, SQLModel


class UnitBase(SQLModel):
    name: str = Field(index=True)


class Unit(UnitBase, table=True):
    id: int = Field(default=None, primary_key=True)
    updated_at: datetime | None = Field(
        default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now}
    )
    created_at: datetime | None = Field(default_factory=datetime.now)


class UnitCreate(UnitBase):
    pass


class UnitRead(UnitBase):
    id: int
    name: str | None = None


class UnitUpdate(UnitBase):
    name: str | None = None


class UnitMaterial(SQLModel):
    name: str