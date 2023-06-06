from fastapi import APIRouter
from mirel.presentation.api.v1 import (
    product,
    type_solution,
    type_object,
    article,
    image,
)
from mirel.config.settings import Settings

settings = Settings()

router = APIRouter()
router.include_router(product.router, prefix="/products", tags=["products"])
router.include_router(article.router, prefix="/articles", tags=["articles"])
router.include_router(
    type_solution.router, prefix="/type_solutions", tags=["type_solutions"]
)
router.include_router(
    type_object.router, prefix="/type_objects", tags=["type_objects"]
)
router.include_router(image.router, prefix="/images", tags=["images"])
