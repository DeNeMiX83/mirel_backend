from typing import Protocol


class Service(Protocol):
    async def create_image(self, path_to_image: str) -> str:
        raise NotImplementedError

    async def get_image(seld, filename: str) -> str:
        raise NotImplementedError
