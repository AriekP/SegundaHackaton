from sqlalchemy.orm import Session
from app.models.role import Rol, UsuarioRol
from app.models.user import Usuario
from app.schemas.role import RolCreate

def crear_rol(db: Session, rol: RolCreate):
    nuevo_rol = Rol(nombre=rol.nombre)
    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)
    return nuevo_rol

def asignar_rol_a_usuario(db: Session, usuario_id: int, rol_id: int):
    relacion = UsuarioRol(usuario_id=usuario_id, rol_id=rol_id)
    db.add(relacion)
    db.commit()
    return relacion

def obtener_roles_de_usuario(db: Session, usuario_id: int):
    return db.query(UsuarioRol).filter(UsuarioRol.usuario_id == usuario_id).all()

def tiene_rol(db: Session, usuario_id: int, rol_nombre: str):
    return db.query(Rol).join(UsuarioRol).filter(UsuarioRol.usuario_id == usuario_id, Rol.nombre == rol_nombre).first() is not None
