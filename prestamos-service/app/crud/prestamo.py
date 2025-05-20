from sqlalchemy.orm import Session
from app.models.prestamo import Prestamo
from app.schemas.prestamo import PrestamoCreate

def crear_prestamo(db: Session, data: PrestamoCreate):
    nuevo = Prestamo(**data.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_prestamos(db: Session):
    return db.query(Prestamo).all()

def obtener_prestamo(db: Session, prestamo_id: int):
    return db.query(Prestamo).filter(Prestamo.id == prestamo_id).first()

def actualizar_prestamo(db: Session, prestamo_id: int, data: PrestamoCreate):
    prestamo = obtener_prestamo(db, prestamo_id)
    if not prestamo:
        return None
    for key, value in data.model_dump().items():
        setattr(prestamo, key, value)
    db.commit()
    db.refresh(prestamo)
    return prestamo

def eliminar_prestamo(db: Session, prestamo_id: int):
    prestamo = obtener_prestamo(db, prestamo_id)
    if not prestamo:
        return {"ok": False, "message": "No encontrado"}
    db.delete(prestamo)
    db.commit()
    return {"ok": True, "message": "Eliminado"}
