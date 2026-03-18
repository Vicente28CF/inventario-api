from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Electrónicos",
                "descripcion": "Computadoras, tablets y accesorios"
            }
        }
    }

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None

    model_config = {"from_attributes": True}

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int = 0
    stock_minimo: int = 5
    categoria_id: Optional[int] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Laptop Dell XPS 15",
                "descripcion": "Laptop profesional con pantalla OLED",
                "precio": 25000.00,
                "stock": 10,
                "stock_minimo": 3,
                "categoria_id": 1
            }
        }
    }

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock_minimo: Optional[int] = None
    categoria_id: Optional[int] = None
    activo: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "precio": 22000.00,
                "stock_minimo": 5
            }
        }
    }

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

    model_config = {"from_attributes": True}

class MovimientoCreate(BaseModel):
    producto_id: int
    tipo: str
    cantidad: int
    nota: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "producto_id": 1,
                "tipo": "entrada",
                "cantidad": 20,
                "nota": "Reabastecimiento mensual"
            }
        }
    }

class MovimientoOut(BaseModel):
    id: int
    tipo: str
    cantidad: int
    nota: Optional[str] = None
    producto_id: int
    creado_en: datetime

    model_config = {"from_attributes": True}