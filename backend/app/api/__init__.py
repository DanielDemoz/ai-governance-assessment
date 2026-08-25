"""API router aggregation."""

from fastapi import APIRouter

from app.api.assessments import router as assessments_router
from app.api.categories import router as categories_router
from app.api.risks import router as risks_router

api_router = APIRouter()
api_router.include_router(categories_router)
api_router.include_router(assessments_router)
api_router.include_router(risks_router)
