# Packages
# Packages
from fastapi import APIRouter


# Modules
from apis.products import router as products


router = APIRouter(prefix="/api")

router.include_router(products)
