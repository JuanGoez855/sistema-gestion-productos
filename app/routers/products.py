from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.controllers.products import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product
)

from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)

router = APIRouter(
    prefix="/products",
    tags=["Productos"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product_endpoint(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    product = create_product(
        db,
        product_data,
        current_user.id
    )

    if product == "category_not_found":
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return product


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products_endpoint(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: str | None = Query(
        default=None,
        min_length=1
    ),
    category_id: int | None = Query(
        default=None,
        ge=1
    ),
    min_price: float | None = Query(
        default=None,
        ge=0
    ),
    max_price: float | None = Query(
        default=None,
        ge=0
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=400,
            detail="El precio mínimo no puede ser mayor que el precio máximo"
        )

    return get_products(
        db,
        skip,
        limit,
        name,
        category_id,
        min_price,
        max_price
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = get_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return product


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product_endpoint(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    product = update_product(
        db,
        product_id,
        product_data
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    if product == "category_not_found":
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return product


@router.delete(
    "/{product_id}"
)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    product = delete_product(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {
        "success": True,
        "message": "Producto eliminado correctamente"
    }
