from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
token_dependency = Depends(oauth2_scheme)
db_dependency = Depends(get_db)


def get_current_user(
    token: str = token_dependency,
    db: Session = db_dependency,
) -> Usuario:
    email = decode_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not user.activo:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


current_user_dependency = Depends(get_current_user)


def require_admin(current_user: Usuario = current_user_dependency) -> Usuario:
    if current_user.rol != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador",
        )
    return current_user
