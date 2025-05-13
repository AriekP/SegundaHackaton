from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter()

@router.get("/transacciones/", response_model=list[schemas.TransaccionResponse])
def obtener_todas_las_transacciones(db: Session = Depends(database.get_db)):
    return crud.obtener_todas_las_transacciones(db)

@router.get("/transacciones/{transaccion_id}", response_model=schemas.TransaccionResponse)
def obtener_transaccion(transaccion_id: int, db: Session = Depends(database.get_db)):
    transaccion = crud.obtener_transaccion(db, transaccion_id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion

@router.post("/transacciones/", response_model=schemas.TransaccionResponse)
def crear_transaccion(transaccion: schemas.TransaccionCreate, db: Session = Depends(database.get_db)):
    return crud.crear_transaccion(db, transaccion)

@router.put("/transacciones/{transaccion_id}", response_model=schemas.TransaccionResponse)
def actualizar_transaccion(transaccion_id: int, transaccion: schemas.TransaccionCreate, db: Session = Depends(database.get_db)):
    return crud.actualizar_transaccion(db, transaccion_id, transaccion)

@router.delete("/transacciones/{transaccion_id}")
def eliminar_transaccion(transaccion_id: int, db: Session = Depends(database.get_db)):
    crud.eliminar_transaccion(db, transaccion_id)
    return {"message": "Transacción eliminada exitosamente"}