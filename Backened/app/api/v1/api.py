from fastapi import APIRouter
from app.api.v1.endpoints import aws
from app.api.v1.endpoints import kubernetes
from app.api.v1.endpoints import vmware
from app.api.v1.endpoints import openstack
from app.api.v1.endpoints import template
from app.api.v1.endpoints import cost_management

api_router = APIRouter()

api_router.include_router(aws.router, prefix="/aws", tags=["aws"])
api_router.include_router(kubernetes.router, prefix="/kubernetes", tags=["kubernetes"])
api_router.include_router(vmware.router, prefix="/vmware", tags=["vmware"])
api_router.include_router(openstack.router, prefix="/openstack", tags=["openstack"])
api_router.include_router(template.router, prefix="/templates", tags=["templates"])
api_router.include_router(cost_management.router, prefix="/cost-management", tags=["cost-management"]) 