from .base import Hаndler
from mirel.core.dto import ForwardingFeedbackData
from mirel.core.protocols import EmailSender


class ForwardingFeedbackHandler(Hаndler[ForwardingFeedbackData, None]):
    def __init__(self, email_sender: EmailSender):
        self._email_sender = email_sender

    async def execute(self, data: ForwardingFeedbackData) -> None:
        await self._email_sender.forwarding_feedback(data)
