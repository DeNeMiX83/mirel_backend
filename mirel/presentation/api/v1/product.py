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
from mirel.core.entities import ProductId
from mirel.core.exceptions import UnsupportedImageFormat
from mirel.core.dto import (
    ProductCreate as ProductCreateForHandler,
    ProductAddImage as ProductAddImageForHandler,
    ProductGetAll as ProductGetAllForHandler,
    ProductGet as ProductGetForHandler,
    ProductGetByFilters as ProductGetByFiltersForHandler,
    ProductReturn,
)
from mirel.core.handlers import (
    ProductCreateHandler,
    ProductAddImageHandler,
    ProductGetAllHandler,
    ProductGetHandler,
    ProductGetByFiltersHandler,
)
from mirel.presentation.api.di.stubs import (
    provide_settings_stub,
    provide_product_create_handler_stub,
    provide_product_add_image_handler_stub,
    provide_product_get_handler_stub,
    provide_product_get_all_handler_stub,
    provide_product_get_by_filters_handler_stub,
)
from .field_templates import get_pagination_fields
from .work_with_files import save_file
from .dto import (
    PaginationResponse,
    ProductCreate,
    ProductGetByFilters,
)

router = APIRouter()


def get_product_from_form(product: str = Form(...)):
    try:
        model = ProductCreate.parse_raw(product)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return model


@router.post(
    path="/", status_code=status.HTTP_201_CREATED, response_model=None
)
async def create_product(
    response: Response,
    settings: Settings = Depends(provide_settings_stub),
    product: ProductCreate = Depends(get_product_from_form),
    preview_image: UploadFile = File(..., description="Preview Image"),
    image: UploadFile = File(..., description="Image"),
    handler: ProductCreateHandler = Depends(
        provide_product_create_handler_stub
    ),
):
    path_to_preview_image = await save_file(
        preview_image,
        settings.path_to_folder_for_save_image,
        "product_preview",
    )
    path_to_image = await save_file(
        image, settings.path_to_folder_for_save_image, "product"
    )
    try:
        product_return = await handler.execute(
            ProductCreateForHandler(
                title=product.title,
                company_names=product.company_names,
                type_solution_names=product.type_solution_names,
                type_object_names=product.type_object_names,
                year_implementation=product.year_implementation,
                preview_description=product.preview_description,
                description=product.description,
                path_to_preview_image=path_to_preview_image,
                path_to_image=path_to_image,
            )
        )
    except UnsupportedImageFormat:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неподдерживаемый формат файла."
            + " Допустимые форматы: png, jpg, jpeg",
        )
    return product_return


@router.post(
    path="/{product_id:str}/image",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
)
async def product_add_image(
    response: Response,
    product_id: ProductId,
    image: UploadFile = File(..., description="Image"),
    handler: ProductAddImageHandler = Depends(
        provide_product_add_image_handler_stub
    ),
    settings: Settings = Depends(provide_settings_stub),
):
    path_to_image = await save_file(
        image, settings.path_to_folder_for_save_image, "product"
    )
    try:
        await handler.execute(
            ProductAddImageForHandler(
                product_id=product_id,
                path_to_image=path_to_image,
            )
        )
    except UnsupportedImageFormat:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Неподдерживаемый формат файла."
            + " Допустимые форматы: png, jpg, jpeg",
        )
    return "ok"


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse[ProductReturn],
)
async def get_all_product(
    response: Response,
    pagination_fields: Tuple[int, int] = Depends(get_pagination_fields),
    handler: ProductGetAllHandler = Depends(
        provide_product_get_all_handler_stub
    ),
):
    products = await handler.execute(ProductGetAllForHandler())

    page, size = pagination_fields
    response_data = PaginationResponse.get_by_items(
        items=products,
        page=page,
        size=size,
    )
    return response_data


@router.get(
    path="/{id:str}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[ProductReturn],
)
async def get_product(
    response: Response,
    id: ProductId,
    handler: ProductGetHandler = Depends(provide_product_get_handler_stub),
):
    products = await handler.execute(ProductGetForHandler(id=id))
    return products


@router.post(
    path="/filter",
    status_code=status.HTTP_200_OK,
    response_model=PaginationResponse[ProductReturn],
)
async def get_product_by_filters(
    response: Response,
    filters: ProductGetByFilters,
    pagination_fields: Tuple[int, int] = Depends(get_pagination_fields),
    handler: ProductGetByFiltersHandler = Depends(
        provide_product_get_by_filters_handler_stub
    ),
):
    page, size = pagination_fields
    products = await handler.execute(
        ProductGetByFiltersForHandler(
            company=filters.company,
            type_solution=filters.type_solution,
            type_object=filters.type_object,
            year_implementation=filters.year_implementation,
        )
    )

    response_data = PaginationResponse.get_by_items(
        items=products,
        page=page,
        size=size,
    )
    return response_data
