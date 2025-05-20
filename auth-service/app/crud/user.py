from sqlalchemy.orm import Session
from app.models.user import Usuario
from app.schemas.user import UsuarioCrear
from app.auth.security import get_password_hash

def crear_usuario(db: Session, usuario: UsuarioCrear):
    hashed_pw = get_password_hash(usuario.password)
    nuevo_usuario = Usuario(correo=usuario.correo, hashed_password=hashed_pw, cliente_id=usuario.cliente_id)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def obtener_usuario_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def obtener_usuario(db: Session, id: int):
    return db.query(Usuario).filter(Usuario.id == id).first()
