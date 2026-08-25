"""Category API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)) -> list[Category]:
    return (
        db.query(Category)
        .options(joinedload(Category.questions))
        .order_by(Category.sort_order)
        .all()
    )
