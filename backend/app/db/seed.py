"""Seed categories and questions into the database."""

from sqlalchemy.orm import Session

from app.db.seed_data import CATEGORY_SEED, QUESTION_SEED
from app.models.category import Category
from app.models.question import Question, RiskLevel


def seed_reference_data(db: Session) -> dict[str, int]:
    """Insert or update categories and questions. Returns counts."""
    category_count = 0
    question_count = 0

    category_by_code: dict[str, Category] = {}

    for cat_data in CATEGORY_SEED:
        category = db.query(Category).filter(Category.code == cat_data["code"]).first()
        if category is None:
            category = Category(**cat_data)
            db.add(category)
            category_count += 1
        else:
            for key, value in cat_data.items():
                setattr(category, key, value)
        category_by_code[cat_data["code"]] = category

    db.flush()

    for category_code, questions in QUESTION_SEED.items():
        category = category_by_code[category_code]
        for index, q_data in enumerate(questions, start=1):
            question = db.query(Question).filter(Question.code == q_data["code"]).first()
            payload = {
                "category_id": category.id,
                "text": q_data["text"],
                "governance_objective": q_data["governance_objective"],
                "risk_level": RiskLevel(q_data["risk_level"]),
                "recommendation_key": q_data["recommendation_key"],
                "sort_order": index,
            }
            if question is None:
                db.add(Question(code=q_data["code"], **payload))
                question_count += 1
            else:
                for key, value in payload.items():
                    setattr(question, key, value)

    db.commit()
    return {"categories": category_count, "questions": question_count}
