from fastapi import APIRouter
from mirel.presentation.api.v1 import product, article, image
from mirel.config.settings import Settings

settings = Settings()

router = APIRouter(prefix=settings.root_path + settings.api_url)
router.include_router(product.router, prefix="/products", tags=["products"])
router.include_router(article.router, prefix="/articles", tags=["articles"])
router.include_router(image.router, prefix="/images", tags=["images"])
