from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nombre: Annotated[str, Field(min_length=2, max_length=80)]
    descripcion: Annotated[str, Field(max_length=255)] | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Electrónicos",
                "descripcion": "Computadoras, tablets y accesorios",
            }
        }
    }


class CategoriaOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

    model_config = {"from_attributes": True}


class ProductoCreate(BaseModel):
    nombre: Annotated[str, Field(min_length=2, max_length=120)]
    descripcion: Annotated[str, Field(max_length=255)] | None = None
    precio: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
    stock: Annotated[int, Field(ge=0)] = 0
    stock_minimo: Annotated[int, Field(ge=1)] = 5
    categoria_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Laptop Dell XPS 15",
                "descripcion": "Laptop profesional con pantalla OLED",
                "precio": 25000.00,  # noqa: ERA001
                "stock": 10,
                "stock_minimo": 3,
                "categoria_id": 1,
            }
        }
    }


class ProductoUpdate(BaseModel):
    nombre: Annotated[str, Field(min_length=2, max_length=120)] | None = None
    descripcion: Annotated[str, Field(max_length=255)] | None = None
    precio: Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)] | None = None
    stock_minimo: Annotated[int, Field(ge=1)] | None = None
    categoria_id: int | None = None
    activo: bool | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "precio": 22000.00,  # noqa: ERA001
                "stock_minimo": 5,
            }
        }
    }


class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    precio: Decimal
    stock: int
    stock_minimo: int
    activo: bool
    categoria: CategoriaOut | None = None
    creado_en: datetime

    model_config = {"from_attributes": True}


class MovimientoCreate(BaseModel):
    producto_id: int
    tipo: Literal["entrada", "salida"]
    cantidad: Annotated[int, Field(ge=1)]
    nota: Annotated[str, Field(max_length=255)] | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "producto_id": 1,
                "tipo": "entrada",
                "cantidad": 20,
                "nota": "Reabastecimiento mensual",
            }
        }
    }


class MovimientoOut(BaseModel):
    id: int
    tipo: str
    cantidad: int
    nota: str | None = None
    producto_id: int
    creado_en: datetime

    model_config = {"from_attributes": True}


class AlertaStockOut(BaseModel):
    id: int
    nombre: str
    stock_actual: int
    stock_minimo: int
    alerta: str
