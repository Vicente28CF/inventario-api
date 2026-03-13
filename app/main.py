from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, productos, inventario

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventario API",
    description="API REST para gestión de inventario",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(inventario.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Inventario API corriendo"}