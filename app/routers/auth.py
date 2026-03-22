from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import Token, UsuarioCreate, UsuarioOut
from app.services.auth import authenticate_user, build_access_token, register_user

limiter = Limiter(
    key_func=get_remote_address,
    enabled=not settings.TESTING,
)
db_dependency = Depends(get_db)
current_user_dependency = Depends(get_current_user)
oauth2_form_dependency = Depends()

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/registro",
    response_model=UsuarioOut,
    status_code=201,
    summary="Registrar nuevo usuario",
    description=(
        "Crea una cuenta nueva. El rol por defecto es **viewer**. "
        "Solo un admin puede promover a otro usuario. "
        "Límite: **5 registros por minuto** por IP."
    ),
)
@limiter.limit("5/minute")
def registro(
    request: Request,
    datos: UsuarioCreate,
    db: Session = db_dependency,
):
    try:
        usuario = register_user(db, datos)
        db.commit()
        return usuario
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al registrar usuario") from err


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description=(
        "Retorna un **access token JWT**. "
        "Úsalo en el header `Authorization: Bearer <token>` "
        "para endpoints protegidos. "
        "Límite: **10 intentos por minuto** por IP."
    ),
)
@limiter.limit("10/minute")
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = oauth2_form_dependency,
    db: Session = db_dependency,
):
    usuario = authenticate_user(db, form.username, form.password)
    return build_access_token(usuario)


@router.get(
    "/me",
    response_model=UsuarioOut,
    summary="Usuario actual",
    description=(
        "Retorna los datos del usuario autenticado "
        "según el token JWT enviado."
    ),
)
def me(current_user: Usuario = current_user_dependency):
    return current_user
