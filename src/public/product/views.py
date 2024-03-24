from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.database import get_session
from src.public.product.crud import (
    create_product_crud,
    delete_product,
    read_product,
    read_products,
    update_product_crud,
)
from src.public.product.models import ProductCreate, ProductRead, ProductUpdate
from src.utils.logger import logger_config

router = APIRouter()

logger = logger_config(__name__)


@router.post("", response_model=ProductRead)
async def create_products(product: ProductCreate, db: Session = Depends(get_session)):
    product = create_product_crud(product=product, db=db)
    return ProductRead(id=product.id, name=product.name, code=product.code, materials=product.material_links)


@router.get("", response_model=list[ProductRead])
async def get_products(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    db: Session = Depends(get_session),
):
    logger.info(f"{__name__}.get_products: triggered")
    products = read_products(offset=offset, limit=limit, db=db)
    return [ProductRead(id=product.id, name=product.name, code=product.code, materials=product.material_links) for product in products]


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.get_a_product.id: {product_id}")
    product = read_product(product_id=product_id, db=db)
    return ProductRead(id=product.id, name=product.name, code=product.code, materials=product.material_links)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.update_a_product.id: {product_id}")
    product = update_product_crud(product_id=product_id, product=product, db=db)
    return ProductRead(id=product.id, name=product.name, code=product.code, materials=product.material_links)


@router.delete("/{product_id}")
def delete_a_product(product_id: int, db: Session = Depends(get_session)):
    logger.info(f"{__name__}.delete_product: {product_id} triggered")
    return delete_product(product_id=product_id, db=db)