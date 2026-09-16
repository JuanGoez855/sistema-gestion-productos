from fastapi import FastAPI

from app.database import Base, engine
from app.models import category, product, user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Productos",
    description="API REST desarrollada con FastAPI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "API funcionando correctamente"
    }