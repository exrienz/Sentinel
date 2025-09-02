from fastapi import APIRouter, Request

from src.application.dependencies.service_dependency import (
    ProductServiceDep,
    ProjectManagementServiceDep,
)
from src.application.schemas.project_management import (
    ProjectResponseSchema,
)

router = APIRouter(prefix="", tags=["General API"])


@router.get("/projects", response_model=list[ProjectResponseSchema])
async def project_lists(request: Request, service: ProjectManagementServiceDep):
    return await service.get_all()


@router.get("/products")
async def product_lists(request: Request, service: ProductServiceDep):
    return await service.get_all_by_filter({})
