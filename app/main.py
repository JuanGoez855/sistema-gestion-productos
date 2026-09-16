from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.exceptions import ProductNotFoundError
from app.models import category, product, user

from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Gestión de Productos",
    description="API REST para la gestión de usuarios, categorías y productos",
    version="1.0.0"
)


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "PRODUCT_NOT_FOUND",
            "message": exc.message,
            "product_id": exc.product_id
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Ocurrió un error interno en el servidor"
        }
    )


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)


@app.get("/", tags=["Inicio"])
def root():
    return {
        "success": True,
        "message": "API funcionando correctamente"
    }