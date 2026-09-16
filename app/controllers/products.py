from sqlalchemy.orm import Session

from app.exceptions import ProductNotFoundError
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


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    category_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str = "id",
    order: str = "asc"
):
    query = db.query(Product)

    if name:
        query = query.filter(
            Product.name.ilike(f"%{name}%")
        )

    if category_id is not None:
        query = query.filter(
            Product.category_id == category_id
        )

    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    sort_columns = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price,
        "stock": Product.stock
    }

    sort_column = sort_columns.get(sort_by)

    if sort_column is None:
        return "invalid_sort"

    if order == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    return query.offset(skip).limit(limit).all()


def get_product(
    db: Session,
    product_id: int
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise ProductNotFoundError(product_id)

    return product


def update_product(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
):
    product = get_product(
        db,
        product_id
    )

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
    product = get_product(
        db,
        product_id
    )

    db.delete(product)
    db.commit()

    return product