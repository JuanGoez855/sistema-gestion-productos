from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.categories import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category
)

from app.database import get_db
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)


router = APIRouter(
    prefix="/categories",
    tags=["Categorías"]
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category_endpoint(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    category = create_category(
        db,
        category_data
    )

    if category is None:
        raise HTTPException(
            status_code=400,
            detail="La categoría ya existe"
        )

    return category


@router.get(
    "/",
    response_model=list[CategoryResponse]
)
def get_categories_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_categories(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = get_category(
        db,
        category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category_endpoint(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    category = update_category(
        db,
        category_id,
        category_data
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    if category == "duplicate":
        raise HTTPException(
            status_code=400,
            detail="La categoría ya existe"
        )

    return category


@router.delete(
    "/{category_id}"
)
def delete_category_endpoint(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    category = delete_category(
        db,
        category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return {
        "success": True,
        "message": "Categoría eliminada correctamente"
    }