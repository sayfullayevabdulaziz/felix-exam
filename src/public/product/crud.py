from fastapi import HTTPException, status
from sqlmodel import Session, select


from src.public.material.crud import read_material
from src.public.product.models import Product, ProductCreate, ProductUpdate, ProductAddMaterials
from src.utils.generic_models import ProductMaterialLink
from src.utils.logger import logger_config


logger = logger_config(__name__)


def create_product_crud(product: ProductCreate, db: Session):
    product_to_db = Product(name=product.name, code=product.code)
    # logger.info(product_to_db)
    # db.add(product_to_db)
    # db.commit()
    # db.refresh(product_to_db)
    # logger.info(f"{__name__}.product_created: {product}")
    
    for material in product.materials:
        material_from_db = read_material(material_id=material.material_id, db=db)
        db.add(product_to_db)
        db.commit()
        db.refresh(product_to_db)
        logger.info(f"{__name__}.product_created: {product}")

        product_materials = ProductMaterialLink(product=product_to_db, material=material_from_db, quantity=material.quantity)    
        db.add(product_materials)
        db.commit()

    return product_to_db


def read_products(db: Session, offset: int = 0, limit: int = 20):
    products = db.exec(select(Product).offset(offset).limit(limit)).all()
    return products


def read_product(product_id: int, db: Session):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id: {product_id}",
        )
    return product


def update_product_crud(product_id: int, product: ProductUpdate, db: Session):
    product_to_update = db.get(Product, product_id)
    if not product_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id: {product_id}",
        )

    product_data = product.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(product_to_update, key, value)

    db.add(product_to_update)
    db.commit()
    db.refresh(product_to_update)
    return product_to_update


def delete_product(product_id: int, db: Session):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id: {product_id}",
        )

    db.delete(product)
    db.commit()