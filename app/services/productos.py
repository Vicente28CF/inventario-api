from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.producto import Categoria, Producto


def get_categoria_or_404(db: Session, categoria_id: int) -> Categoria:
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


def validate_categoria_id(db: Session, categoria_id: int | None) -> None:
    if categoria_id is not None:
        get_categoria_or_404(db, categoria_id)


def get_producto_or_404(db: Session, producto_id: int) -> Producto:
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


def get_active_producto_or_404(db: Session, producto_id: int) -> Producto:
    producto = get_producto_or_404(db, producto_id)
    if not producto.activo:
        raise HTTPException(status_code=409, detail="El producto está inactivo")
    return producto
