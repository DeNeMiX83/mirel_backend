from os import remove
from io import BytesIO
from typing import Annotated, Dict
from pydantic import ValidationError
from yadisk.exceptions import PathNotFoundError
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from mirel.config.settings import Settings
from mirel.core.dto import (
    ImageGet as ImageGetForHandler,
)
from mirel.core.handlers import ImageGetHandler
from mirel.presentation.api.di.stubs import (
    provide_image_get_handler_stub,
)

router = APIRouter()


@router.get("/{filename:str}")
async def get_image(
    filename: str,
    handler: ImageGetHandler = Depends(provide_image_get_handler_stub),
):
    try:
        image = await handler.execute(ImageGetForHandler(filename=filename))
    except PathNotFoundError:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не найден"
        )
    f = open(image, "rb").read()
    remove(image)
    return StreamingResponse(BytesIO(f), media_type="image/jpeg")
