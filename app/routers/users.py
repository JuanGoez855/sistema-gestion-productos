from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controllers.users import (
    create_user,
    delete_user,
    get_user,
    get_users,
    update_user
)
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = create_user(db, user_data)

    if user is None:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    return user


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users_endpoint(
    db: Session = Depends(get_db)
):
    return get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user_endpoint(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = update_user(db, user_id, user_data)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


@router.delete(
    "/{user_id}"
)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = delete_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "success": True,
        "message": "Usuario eliminado correctamente"
    }