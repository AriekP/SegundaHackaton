from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.role import RolCreate, RolOut
from app.crud import role as crud_role

router = APIRouter()

@router.post("/roles/", response_model=RolOut)
def crear_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return crud_role.crear_rol(db, rol)

@router.post("/usuarios/{usuario_id}/roles/{rol_id}")
def asignar_rol(usuario_id: int, rol_id: int, db: Session = Depends(get_db)):
    return crud_role.asignar_rol_a_usuario(db, usuario_id, rol_id)

@router.get("/usuarios/{usuario_id}/roles")
def obtener_roles(usuario_id: int, db: Session = Depends(get_db)):
    return crud_role.obtener_roles_de_usuario(db, usuario_id)

@router.get("/usuarios/{usuario_id}/tiene-rol/{rol}")
def tiene_rol(usuario_id: int, rol: str, db: Session = Depends(get_db)):
    return {"tiene_rol": crud_role.tiene_rol(db, usuario_id, rol)}
