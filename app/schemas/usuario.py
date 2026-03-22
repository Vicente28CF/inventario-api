from pydantic import BaseModel, EmailStr


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "nombre": "Vicente Cayetano",
                "email": "vicente@email.com",
                "password": "miclave123"
            }
        }
    }

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    activo: bool

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
