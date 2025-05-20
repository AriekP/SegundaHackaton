from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.prestamo import PrestamoCreate, PrestamoOut
from app.database import get_db
from app.crud import prestamo as crud

router = APIRouter()

@router.post("/", response_model=PrestamoOut)
def crear_prestamo(data: PrestamoCreate, db: Session = Depends(get_db)):
    return crud.crear_prestamo(db, data)

@router.get("/", response_model=list[PrestamoOut])
def listar_prestamos(db: Session = Depends(get_db)):
    return crud.listar_prestamos(db)

@router.get("/{prestamo_id}", response_model=PrestamoOut)
def obtener_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    prestamo = crud.obtener_prestamo(db, prestamo_id)
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo

@router.put("/{prestamo_id}", response_model=PrestamoOut)
def actualizar_prestamo(prestamo_id: int, data: PrestamoCreate, db: Session = Depends(get_db)):
    return crud.actualizar_prestamo(db, prestamo_id, data)

@router.delete("/{prestamo_id}")
def eliminar_prestamo(prestamo_id: int, db: Session = Depends(get_db)):
    return crud.eliminar_prestamo(db, prestamo_id)
