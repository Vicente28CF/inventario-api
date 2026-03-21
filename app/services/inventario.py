from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.movimiento import Movimiento
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.schemas.producto import MovimientoCreate
from app.services.productos import get_active_producto_or_404


def registrar_movimiento_stock(
    db: Session,
    datos: MovimientoCreate,
    current_user: Usuario,
) -> Movimiento:
    producto = get_active_producto_or_404(db, datos.producto_id)

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
        usuario_id=current_user.id,
    )
    db.add(movimiento)
    db.flush()
    db.refresh(movimiento)
    return movimiento


def obtener_alertas_stock(db: Session) -> list[Producto]:
    return (
        db.query(Producto)
        .filter(Producto.stock <= Producto.stock_minimo, Producto.activo.is_(True))
        .all()
    )
