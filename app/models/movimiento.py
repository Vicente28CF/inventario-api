from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class TipoMovimiento(str, enum.Enum):
    entrada = "entrada"
    salida  = "salida"

class Movimiento(Base):
    __tablename__ = "movimientos"
    

    id        = Column(Integer, primary_key=True, index=True)
    tipo      = Column(Enum(TipoMovimiento), nullable=False)
    cantidad  = Column(Integer, nullable=False)
    nota      = Column(String, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    producto = relationship("Producto", back_populates="movimientos")
    usuario  = relationship("Usuario")