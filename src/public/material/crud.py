from fastapi import HTTPException, status
from sqlmodel import Session, select


from src.public.material.models import Material, MaterialCreate, MaterialUpdate


def create_material_crud(material: MaterialCreate, db: Session):
    material_to_db = Material.model_validate(material)
    db.add(material_to_db)
    db.commit()
    db.refresh(material_to_db)
    return material_to_db


def read_materials(db: Session, offset: int = 0, limit: int = 20):
    materials = db.exec(select(Material).offset(offset).limit(limit)).all()
    return materials


def read_material(material_id: int, db: Session):
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"material not found with id: {material_id}",
        )
    return material


def update_material_crud(material_id: int, material: MaterialUpdate, db: Session):
    material_to_update = db.get(Material, material_id)
    if not material_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"material not found with id: {material_id}",
        )

    material_data = material.model_dump(exclude_unset=True)
    for key, value in material_data.items():
        setattr(material_to_update, key, value)

    db.add(material_to_update)
    db.commit()
    db.refresh(material_to_update)
    return material_to_update


def delete_material(material_id: int, db: Session):
    material = db.get(Material, material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"material not found with id: {material_id}",
        )

    db.delete(material)
    db.commit()