from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UsuarioCrear, UsuarioOut
from app.auth.security import verify_password, create_access_token
from app.auth.dependencies import get_current_user
from app.crud import user as crud_user

router = APIRouter()

@router.post("/signup", response_model=UsuarioOut)
def signup(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    if crud_user.obtener_usuario_por_correo(db, usuario.correo):
        raise HTTPException(status_code=400, detail="Usuario ya registrado")
    return crud_user.crear_usuario(db, usuario)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = crud_user.obtener_usuario_por_correo(db, form_data.username)
    if not usuario or not verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": usuario.correo})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioOut)
def me(usuario=Depends(get_current_user)):
    return usuario
