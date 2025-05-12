# app/routers/transacciones.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter()

@router.post("/transacciones/", response_model=schemas.TransaccionResponse)
def crear_transaccion(transaccion: schemas.TransaccionCreate, db: Session = Depends(database.get_db)):
    return crud.crear_transaccion(db, transaccion)

@router.get("/transacciones/{cuenta_id}", response_model=list[schemas.TransaccionResponse])
def obtener_transacciones(cuenta_id: int, db: Session = Depends(database.get_db)):
    transacciones = crud.obtener_transacciones(db, cuenta_id)
    if not transacciones:
        raise HTTPException(status_code=404, detail="Transacciones no encontradas")
    return transacciones