from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from mirel.core.dto import ForwardingFeedbackData
from mirel.core.handlers import (
    ForwardingFeedbackHandler,
)
from mirel.presentation.api.di.stubs import (
    provide_forwarding_feedback_handler_stub,
)
from .dto import ForwardingFeedbackData as ForwardingFeedbackDataForQuery

router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def forwarding_feedback(
    response: Response,
    data: ForwardingFeedbackDataForQuery,
    handler: ForwardingFeedbackHandler = Depends(
        provide_forwarding_feedback_handler_stub
    ),
):
    await handler.execute(
        ForwardingFeedbackData(
            name=data.name,
            email=data.email,
            telephone=data.telephone,
            msg=data.msg,
        )
    )
    return "ok"
