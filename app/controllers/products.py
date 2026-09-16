from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(
    db: Session,
    product_data: ProductCreate,
    user_id: int
):
    category = db.query(Category).filter(
        Category.id == product_data.category_id
    ).first()

    if not category:
        return "category_not_found"

    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        category_id=product_data.category_id,
        created_by_id=user_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session):
    return db.query(Product).all()


def get_product(
    db: Session,
    product_id: int
):
    return db.query(Product).filter(
        Product.id == product_id
    ).first()


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):
    product = get_product(db, product_id)

    if not product:
        return None

    data = product_data.model_dump(
        exclude_unset=True
    )

    if "category_id" in data:
        category = db.query(Category).filter(
            Category.id == data["category_id"]
        ).first()

        if not category:
            return "category_not_found"

    for key, value in data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(
    db: Session,
    product_id: int
):
    product = get_product(db, product_id)

    if not product:
        return None

    db.delete(product)
    db.commit()

    return product