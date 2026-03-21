from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.movimiento import Movimiento
from app.schemas.producto import AlertaStockOut, MovimientoCreate, MovimientoOut
from app.core.deps import get_current_user
from app.models.usuario import Usuario
from app.services.inventario import obtener_alertas_stock, registrar_movimiento_stock
from app.services.productos import get_producto_or_404

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.post("/movimiento", response_model=MovimientoOut, status_code=201)
def registrar_movimiento(
    datos: MovimientoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    try:
        movimiento = registrar_movimiento_stock(db, datos, current_user)
        db.commit()
        return movimiento
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar movimiento")

@router.get("/movimientos/{producto_id}", response_model=List[MovimientoOut])
def historial_movimientos(
    producto_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    get_producto_or_404(db, producto_id)
    return db.query(Movimiento).filter(Movimiento.producto_id == producto_id).all()

@router.get("/alertas", response_model=List[AlertaStockOut])
def alertas_stock(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user)
):
    productos = obtener_alertas_stock(db)
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
