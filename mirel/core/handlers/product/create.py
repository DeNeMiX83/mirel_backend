from typing import List
from mirel.core.handlers.base import Hаndler
from mirel.core.exceptions import (
    UnsupportedImageFormat,
    TypeObjectNotFoundException,
    TypeSolutionNotFoundException,
    CompanyNotFoundException,
)
from mirel.core.protocols import (
    Commiter,
    ProductGateway,
    ProductCloudGateway,
    TypeObjectGateway,
    TypeSolutionGateway,
    CompanyGateway,
    ImageEditor,
)
from mirel.core.dto import ProductCreate, ProductReturn
from mirel.core.entities import (
    Company,
    TypeObject,
    TypeSolution,
)
from mirel.core.services import ProductService


class ProductCreateHandler(Hаndler[ProductCreate, ProductReturn]):
    def __init__(
        self,
        product_service: ProductService,
        product_gateway: ProductGateway,
        type_object_gateway: TypeObjectGateway,
        type_solution_gateway: TypeSolutionGateway,
        company_gateway: CompanyGateway,
        commiter: Commiter,
        product_cloud_gateway: ProductCloudGateway,
        image_editor: ImageEditor,
    ):
        self._product_service = product_service
        self._product_gateway = product_gateway
        self._type_object_gateway = type_object_gateway
        self._type_solution_gateway = type_solution_gateway
        self._company_gateway = company_gateway
        self._commiter = commiter
        self._product_cloud_gateway = product_cloud_gateway
        self._image_editor = image_editor

    async def execute(self, data: ProductCreate) -> ProductReturn:
        allowed_formats = ["png", "jpg", "jpeg"]
        preview_image_file_ext = data.path_to_preview_image.split(".")[-1]
        image_file_ext = data.path_to_preview_image.split(".")[-1]
        if (
            preview_image_file_ext not in allowed_formats
            or image_file_ext not in allowed_formats
        ):
            raise UnsupportedImageFormat()

        companies = await self._company_names_to_objects(data.company_names)
        type_objects = await self._type_object_names_to_objects(
            data.type_object_names
        )
        type_soluions = await self._type_solution_names_to_objects(
            data.type_solution_names
        )

        link_to_preview_image = await self._get_link_to_image(
            data.path_to_preview_image
        )
        link_to_image = await self._get_link_to_image(data.path_to_image)

        product = self._product_service.create(
            data,
            link_to_preview_image=link_to_preview_image,
            link_to_image=link_to_image,
            companies=companies,
            type_objects=type_objects,
            type_soluions=type_soluions,
        )

        product_return = await self._product_gateway.create(product)
        await self._commiter.commit()
        return product_return

    async def _company_names_to_objects(
        self, company_names: List[str]
    ) -> List[Company]:
        companies = []
        for company_name in company_names:
            company = await self._company_gateway.get_by_name(company_name)
            if company is None:
                raise CompanyNotFoundException()
            companies.append(company)
        return companies

    async def _type_object_names_to_objects(
        self, type_object_names: List[str]
    ) -> List[TypeObject]:
        type_objects = []
        for type_object_name in type_object_names:
            type_object = await self._type_object_gateway.get_by_name(
                type_object_name
            )
            if type_object is None:
                raise TypeObjectNotFoundException()
            type_objects.append(type_object)
        return type_objects

    async def _type_solution_names_to_objects(
        self, type_solution_names: List[str]
    ) -> List[TypeSolution]:
        type_solutions = []
        for type_solution_name in type_solution_names:
            type_solution = await self._type_solution_gateway.get_by_name(
                type_solution_name
            )
            if type_solution is None:
                raise TypeSolutionNotFoundException()
            type_solutions.append(type_solution)
        return type_solutions

    async def _get_link_to_image(self, path_to_image: str):
        path_to_image = await self._image_editor.optimize(path_to_image)
        link_to_image = await self._product_cloud_gateway.create_image(
            path_to_image
        )
        return link_to_image
