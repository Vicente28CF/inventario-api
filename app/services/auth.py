from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate


def get_user_by_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def register_user(db: Session, datos: UsuarioCreate) -> Usuario:
    if get_user_by_email(db, datos.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        password=hash_password(datos.password),
    )
    db.add(usuario)
    db.flush()
    db.refresh(usuario)
    return usuario


def authenticate_user(db: Session, email: str, password: str) -> Usuario:
    usuario = get_user_by_email(db, email)
    if not usuario or not verify_password(password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )
    return usuario


def build_access_token(usuario: Usuario) -> dict[str, str]:
    token = create_access_token(data={"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
