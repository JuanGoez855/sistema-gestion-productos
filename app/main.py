from fastapi import FastAPI

from app.database import Base, engine
from app.models import category, product, user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Productos",
    description="API REST para la gestión de usuarios, categorías y productos",
    version="1.0.0"
)


@app.get("/", tags=["Inicio"])
def root():
    return {
        "success": True,
        "message": "API funcionando correctamente"
    }