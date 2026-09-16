from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(
    db: Session,
    category_data: CategoryCreate
):
    existing_category = db.query(Category).filter(
        Category.name == category_data.name
    ).first()

    if existing_category:
        return None

    category = Category(
        name=category_data.name
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_categories(db: Session):
    return db.query(Category).all()


def get_category(
    db: Session,
    category_id: int
):
    return db.query(Category).filter(
        Category.id == category_id
    ).first()


def update_category(
    db: Session,
    category_id: int,
    category_data: CategoryUpdate
):
    category = get_category(db, category_id)

    if not category:
        return None

    data = category_data.model_dump(
        exclude_unset=True
    )

    if "name" in data:
        existing_category = db.query(Category).filter(
            Category.name == data["name"],
            Category.id != category_id
        ).first()

        if existing_category:
            return "duplicate"

    for key, value in data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


def delete_category(
    db: Session,
    category_id: int
):
    category = get_category(db, category_id)

    if not category:
        return None

    db.delete(category)
    db.commit()

    return category