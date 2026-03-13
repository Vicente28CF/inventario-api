from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.producto import Producto
from app.models.movimiento import Movimiento, TipoMovimiento
from app.schemas.producto import MovimientoCreate, MovimientoOut
from app.core.deps import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.post("/movimiento", response_model=MovimientoOut, status_code=201)
def registrar_movimiento(
    datos: MovimientoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    producto = db.query(Producto).filter(Producto.id == datos.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if datos.tipo == "salida" and producto.stock < datos.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    if datos.tipo == "entrada":
        producto.stock += datos.cantidad
    else:
        producto.stock -= datos.cantidad

    movimiento = Movimiento(
        producto_id=datos.producto_id,
        tipo=datos.tipo,
        cantidad=datos.cantidad,
        nota=datos.nota,
        usuario_id=current_user.id
    )
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento

@router.get("/movimientos/{producto_id}", response_model=List[MovimientoOut])
def historial_movimientos(
    producto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db.query(Movimiento).filter(Movimiento.producto_id == producto_id).all()

@router.get("/alertas", response_model=List)
def alertas_stock(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    productos = db.query(Producto).filter(
        Producto.stock <= Producto.stock_minimo,
        Producto.activo == True
    ).all()
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "stock_actual": p.stock,
            "stock_minimo": p.stock_minimo,
            "alerta": "stock bajo"
        }
        for p in productos
    ]