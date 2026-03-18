from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import Base, engine

from app.models.usuario import Usuario
from app.models.producto import Categoria, Producto
from app.models.movimiento import Movimiento

Base.metadata.create_all(bind=engine)

from app.routers import auth, productos, inventario

limiter = Limiter(key_func=get_remote_address)

description = """
API REST para gestión de inventario empresarial.

## Autenticación
Registra un usuario y usa `/auth/login` para obtener tu JWT.
Incluye el token en cada request: `Authorization: Bearer <token>`

## Roles
- **admin** — acceso completo (crear, editar, eliminar)
- **viewer** — solo lectura

## Links
- [Repositorio en GitHub](https://github.com/Vicente28CF/inventario-api)
- [Portafolio](https://vcayetano-dev.lovable.app)
"""

app = FastAPI(
    title="Inventario API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Vicente Cayetano",
        "url": "https://vcayetano-dev.lovable.app",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "Autenticación",
            "description": "Registro, login y datos del usuario actual.",
        },
        {
            "name": "Productos",
            "description": "CRUD de productos y categorías. Requiere rol **admin** para escribir.",
        },
        {
            "name": "Inventario",
            "description": "Movimientos de stock, historial y alertas automáticas.",
        },
    ]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(inventario.router)

@app.get("/", tags=["Status"])
def root():
    return {"status": "ok", "message": "Inventario API corriendo"}