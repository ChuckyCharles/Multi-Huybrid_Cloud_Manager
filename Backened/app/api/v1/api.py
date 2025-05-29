from fastapi import APIRouter
from app.api.v1.endpoints import aws

api_router = APIRouter()

api_router.include_router(aws.router, prefix="/aws", tags=["aws"]) 