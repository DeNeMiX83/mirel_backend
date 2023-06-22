from typing import Tuple, Optional
from pydantic import ValidationError
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    File,
    UploadFile,
    Form,
)
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from mirel.config.settings import Settings
from mirel.core.entities import ArticleId
from mirel.core.exceptions import UnsupportedImageFormat
from mirel.core.dto import (
    ArticleCreate as ArticleCreateForHandler,
    ArticleGetAll as ArticleGetAllForHandler,
    ArticleGet as ArticleGetForHandler,
)
from mirel.core.handlers import (
    ArticleCreateHandler,
    ArticleGetAllHandler,
    ArticleGetHandler,
)
from mirel.core.entities import Article
from mirel.presentation.api.di.stubs import (
    provide_settings_stub,
    provide_article_create_handler_stub,
    provide_article_get_handler_stub,
    provide_article_get_all_handler_stub,
)
from .field_templates import get_pagination_fields
from .work_with_files import save_file
from .dto import PaginationResponse, ArticleCreate

router = APIRouter()


def get_article_from_form(article: str = Form(...)):
    try:
        model = ArticleCreate.parse_raw(article)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return model


@router.post(
    path="/", status_code=status.HTTP_201_CREATED, response_model=None
)
async def create_article(
    response: Response,
    settings: Settings = Depends(provide_settings_stub),
    article: ArticleCreate = Depends(get_article_from_form),
    preview_image: UploadFile = File(..., description="Preview Image"),
    image: UploadFile = File(..., description="Image"),
    handler: ArticleCreateHandler = Depends(
        provide_article_create_handler_stub
    ),
):
    path_to_preview_image = await save_file(
        preview_image,
        settings.path_to_folder_for_save_image,
        "article_preview",
    )
    path_to_image = await save_file(
        image, settings.path_to_folder_for_save_image, "article"
    )
    try:
        article_return = await handler.execute(
            ArticleCreateForHandler(
                title=article.title,
                preview_description=article.preview_description,
                description=article.description,
                path_to_preview_image=path_to_preview_image,
                path_to_image=path_to_image,
            )
        )
    except UnsupportedImageFormat:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неподдерживаемый формат файла. "
            + "Допустимые форматы: png, jpg, jpeg",
        )
    return article_return


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse[Article],
)
async def get_all_article(
    response: Response,
    pagination_fields: Tuple[int, int] = Depends(get_pagination_fields),
    handler: ArticleGetAllHandler = Depends(
        provide_article_get_all_handler_stub
    ),
):
    articles = await handler.execute(ArticleGetAllForHandler())

    page, size = pagination_fields
    response_data = PaginationResponse.get_by_items(
        items=articles,
        page=page,
        size=size,
    )
    return response_data


@router.get(
    path="/{id:str}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[Article],
)
async def get_article(
    response: Response,
    id: ArticleId,
    handler: ArticleGetHandler = Depends(provide_article_get_handler_stub),
):
    articles = await handler.execute(ArticleGetForHandler(id=id))
    return articles
