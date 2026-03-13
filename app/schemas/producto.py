from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    stock_minimo: int = 5
    categoria_id: Optional[int] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    stock_minimo: int
    activo: bool
    categoria: Optional[CategoriaOut] = None
    creado_en: datetime

    class Config:
        from_attributes = True

class MovimientoCreate(BaseModel):
    producto_id: int
    tipo: str
    cantidad: int
    nota: Optional[str] = None

class MovimientoOut(BaseModel):
    id: int
    tipo: str
    cantidad: int
    nota: Optional[str] = None
    producto_id: int
    creado_en: datetime

    class Config:
        from_attributes = True