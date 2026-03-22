from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_admin
from app.database import get_db
from app.models.producto import Categoria, Producto
from app.models.usuario import Usuario
from app.schemas.producto import (
    CategoriaCreate,
    CategoriaOut,
    ProductoCreate,
    ProductoOut,
    ProductoUpdate,
)
from app.services.productos import get_producto_or_404, validate_categoria_id

router = APIRouter(prefix="/productos", tags=["Productos"])
db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)
admin_dependency = Depends(require_admin)


@router.post(
    "/categorias",
    response_model=CategoriaOut,
    status_code=201,
    summary="Crear categoría",
    description=(
        "Crea una nueva categoría de productos. "
        "Requiere rol **admin**."
    ),
)
def crear_categoria(
    datos: CategoriaCreate,
    db: Session = db_dependency,
    _: Usuario = admin_dependency,
):
    existe = db.query(Categoria).filter(Categoria.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    cat = Categoria(**datos.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.get(
    "/categorias",
    response_model=list[CategoriaOut],
    summary="Listar categorías",
    description="Retorna todas las categorías disponibles.",
)
def listar_categorias(
    db: Session = db_dependency,
    _: Usuario = current_user_dependency,
):
    return db.query(Categoria).all()


@router.post(
    "/",
    response_model=ProductoOut,
    status_code=201,
    summary="Crear producto",
    description=(
        "Agrega un nuevo producto al inventario. "
        "Requiere rol **admin**."
    ),
)
def crear_producto(
    datos: ProductoCreate,
    db: Session = db_dependency,
    _: Usuario = admin_dependency,
):
    validate_categoria_id(db, datos.categoria_id)
    producto = Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@router.get(
    "/",
    response_model=list[ProductoOut],
    summary="Listar productos",
    description=(
        "Retorna una lista paginada de productos con filtros opcionales. "
        "Filtra por categoria_id, solo_activos, alerta_stock. "
        "Paginación con page y limit (máximo 100 por página)."
    ),
)
def listar_productos(
    db: Session = db_dependency,
    _: Usuario = current_user_dependency,
    categoria_id: int | None = Query(None, description="ID de la categoría a filtrar"),
    solo_activos: bool = Query(True, description="Incluir solo productos activos"),
    alerta_stock: bool = Query(False, description="Incluir solo productos con stock bajo"),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Resultados por página"),
):
    query = db.query(Producto)
    if solo_activos:
        query = query.filter(Producto.activo.is_(True))
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    if alerta_stock:
        query = query.filter(Producto.stock <= Producto.stock_minimo)
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()


@router.get(
    "/{producto_id}",
    response_model=ProductoOut,
    summary="Obtener producto",
    description="Retorna el detalle de un producto por su ID.",
)
def obtener_producto(
    producto_id: int,
    db: Session = db_dependency,
    _: Usuario = current_user_dependency,
):
    return get_producto_or_404(db, producto_id)


@router.patch(
    "/{producto_id}",
    response_model=ProductoOut,
    summary="Actualizar producto",
    description=(
        "Actualiza uno o más campos de un producto existente. "
        "Solo se modifican los campos enviados. "
        "Requiere rol **admin**."
    ),
)
def actualizar_producto(
    producto_id: int,
    datos: ProductoUpdate,
    db: Session = db_dependency,
    _: Usuario = admin_dependency,
):
    producto = get_producto_or_404(db, producto_id)
    validate_categoria_id(db, datos.categoria_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


@router.delete(
    "/{producto_id}",
    status_code=204,
    summary="Desactivar producto",
    description=(
        "Realiza un **soft delete**: el producto se marca como inactivo "
        "pero no se elimina de la base de datos. "
        "Requiere rol **admin**."
    ),
)
def eliminar_producto(
    producto_id: int,
    db: Session = db_dependency,
    _: Usuario = admin_dependency,
):
    producto = get_producto_or_404(db, producto_id)
    producto.activo = False
    db.commit()
