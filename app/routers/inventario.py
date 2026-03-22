from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.movimiento import Movimiento
from app.models.usuario import Usuario
from app.schemas.producto import AlertaStockOut, MovimientoCreate, MovimientoOut
from app.services.inventario import obtener_alertas_stock, registrar_movimiento_stock
from app.services.productos import get_producto_or_404

router = APIRouter(prefix="/inventario", tags=["Inventario"])
db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)


@router.post("/movimiento", response_model=MovimientoOut, status_code=201)
def registrar_movimiento(
    datos: MovimientoCreate,
    db: Session = db_dependency,
    current_user: Usuario = current_user_dependency,
):
    try:
        movimiento = registrar_movimiento_stock(db, datos, current_user)
        db.commit()
        return movimiento
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar movimiento") from err


@router.get("/movimientos/{producto_id}", response_model=list[MovimientoOut])
def historial_movimientos(
    producto_id: int,
    db: Session = db_dependency,
    _: Usuario = current_user_dependency,
):
    get_producto_or_404(db, producto_id)
    return db.query(Movimiento).filter(Movimiento.producto_id == producto_id).all()


@router.get("/alertas", response_model=list[AlertaStockOut])
def alertas_stock(
    db: Session = db_dependency,
    _: Usuario = current_user_dependency,
):
    productos = obtener_alertas_stock(db)
    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "stock_actual": p.stock,
            "stock_minimo": p.stock_minimo,
            "alerta": "stock bajo",
        }
        for p in productos
    ]
