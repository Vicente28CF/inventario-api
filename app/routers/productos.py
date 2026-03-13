from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.producto import Producto, Categoria
from app.schemas.producto import (
    ProductoCreate, ProductoOut, ProductoUpdate,
    CategoriaCreate, CategoriaOut
)
from app.core.deps import get_current_user, require_admin
from app.models.usuario import Usuario

router = APIRouter(prefix="/productos", tags=["Productos"])

# --- Categorías ---

@router.post("/categorias", response_model=CategoriaOut, status_code=201)
def crear_categoria(
    datos: CategoriaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    existe = db.query(Categoria).filter(Categoria.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    cat = Categoria(**datos.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("/categorias", response_model=List[CategoriaOut])
def listar_categorias(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    return db.query(Categoria).all()

# --- Productos ---

@router.post("/", response_model=ProductoOut, status_code=201)
def crear_producto(
    datos: ProductoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    producto = Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@router.get("/", response_model=List[ProductoOut])
def listar_productos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
    categoria_id: Optional[int] = Query(None),
    solo_activos: bool = Query(True),
    alerta_stock: bool = Query(False),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    query = db.query(Producto)
    if solo_activos:
        query = query.filter(Producto.activo == True)
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    if alerta_stock:
        query = query.filter(Producto.stock <= Producto.stock_minimo)
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.patch("/{producto_id}", response_model=ProductoOut)
def actualizar_producto(
    producto_id: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.activo = False
    db.commit()