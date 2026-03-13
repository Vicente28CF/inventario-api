from fastapi import FastAPI
from app.database import Base, engine

# Importa todos los modelos aquí para que SQLAlchemy los registre una sola vez
from app.models.usuario import Usuario
from app.models.producto import Categoria, Producto
from app.models.movimiento import Movimiento

# Crea las tablas
Base.metadata.create_all(bind=engine)

from app.routers import auth, productos, inventario

app = FastAPI(
    title="Inventario API",
    description="API REST para gestión de inventario",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(inventario.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Inventario API corriendo"}