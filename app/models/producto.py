from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)
    creado_en   = Column(DateTime(timezone=True), server_default=func.now())

    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"

    id             = Column(Integer, primary_key=True, index=True)
    nombre         = Column(String, nullable=False, index=True)
    descripcion    = Column(String, nullable=True)
    precio         = Column(Float, nullable=False)
    stock          = Column(Integer, default=0)
    stock_minimo   = Column(Integer, default=5)
    activo         = Column(Boolean, default=True)
    creado_en      = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    categoria    = relationship("Categoria", back_populates="productos")
    movimientos  = relationship("Movimiento", back_populates="producto")