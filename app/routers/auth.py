from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post(
    "/registro",
    response_model=UsuarioOut,
    status_code=201,
    summary="Registrar nuevo usuario",
    description="Crea una cuenta nueva. El rol por defecto es **viewer**. Límite: **5 registros por minuto** por IP.",
)
@limiter.limit("5/minute")
def registro(request: Request, datos: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        password=hash_password(datos.password)
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Retorna un **access token JWT**. Límite: **10 intentos por minuto** por IP para prevenir fuerza bruta.",
)
@limiter.limit("10/minute")
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not usuario or not verify_password(form.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    token = create_access_token(data={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get(
    "/me",
    response_model=UsuarioOut,
    summary="Usuario actual",
    description="Retorna los datos del usuario autenticado según el token JWT enviado.",
)
def me(current_user: Usuario = Depends(get_current_user)):
    return current_user