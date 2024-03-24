from fastapi import APIRouter

from src.public.unit import views as units
from src.public.material import views as materials
from src.public.product import views as products
from src.public.warehouse import views as warehouse

api = APIRouter()


api.include_router(
    units.router,
    prefix="/units",
    tags=["Units"]
)

api.include_router(
    materials.router,
    prefix="/materials",
    tags=["Material"]
)

api.include_router(
    products.router,
    prefix="/products",
    tags=["Product"]
)

api.include_router(
    warehouse.router,
    prefix="/warehouse",
    tags=["Warehouse"]
)