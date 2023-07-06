from typing import Protocol, Optional, List
from .dto import (
    ProductGetByFilters,
    ProductReturn,
    ForwardingFeedbackData,
)
from .entities import (
    Product,
    ProductId,
    Article,
    ArticleId,
    TypeSolution,
    TypeObject,
    Company,
)


class ProductGateway(Protocol):
    async def get(self, doc_id: ProductId) -> Optional[Product]:
        raise NotImplementedError

    async def get_all(self) -> List[ProductReturn]:
        raise NotImplementedError

    async def get_by_filters(
        self, data: ProductGetByFilters
    ) -> List[ProductReturn]:
        raise NotImplementedError

    async def create(self, data: Product) -> ProductReturn:
        raise NotImplementedError

    async def add_image(
        self, product_id: ProductId, link_to_image: str
    ) -> None:
        raise NotImplementedError

    async def update(self, data: Product):
        raise NotImplementedError


class ArticleGateway(Protocol):
    async def get(self, doc_id: ArticleId) -> Optional[Article]:
        raise NotImplementedError

    async def get_all(self) -> List[Article]:
        raise NotImplementedError

    async def search(self, text: str) -> List[Article]:
        raise NotImplementedError

    async def create(self, data: Article):
        raise NotImplementedError


class TypeSolutionGateway(Protocol):
    async def create(self, data: TypeSolution):
        raise NotImplementedError

    async def get_by_name(self, name: str) -> Optional[TypeSolution]:
        raise NotImplementedError

    async def get_all(self) -> List[TypeSolution]:
        raise NotImplementedError


class TypeObjectGateway(Protocol):
    async def create(self, data: TypeObject):
        raise NotImplementedError

    async def get_by_name(self, name: str) -> Optional[TypeObject]:
        raise NotImplementedError

    async def get_all(self) -> List[TypeObject]:
        raise NotImplementedError


class CompanyGateway(Protocol):
    async def create(self, data: Company):
        raise NotImplementedError

    async def get_by_name(self, name: str) -> Optional[Company]:
        raise NotImplementedError

    async def get_all(self) -> List[Company]:
        raise NotImplementedError


class Commiter(Protocol):
    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError


class ProductCloudGateway(Protocol):
    async def create_preview_image(self, file: str) -> str:
        raise NotImplementedError

    async def create_image(self, file: str) -> str:
        raise NotImplementedError


class ArticleCloudGateway(Protocol):
    async def create_preview_image(self, file: str) -> str:
        raise NotImplementedError

    async def create_image(self, file: str) -> str:
        raise NotImplementedError


class ImageEditor(Protocol):
    async def optimize(self, path_to_photo: str):
        raise NotImplementedError


class ImageCloudGateway(Protocol):
    async def get_image(self, path_to_image: str) -> str:
        raise NotImplementedError


class EmailSender(Protocol):
    async def forwarding_feedback(self, data: ForwardingFeedbackData) -> None:
        raise NotImplementedError
