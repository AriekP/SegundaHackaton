import random
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

def validar_cuenta(cuenta_id: int) -> bool:
    # Simulación temporal de que las cuentas existen
    cuentas_validas = [1, 2, 3, 4, 5]  # IDs de cuentas simuladas
    return cuenta_id in cuentas_validas

def crear_transaccion(db: Session, transaccion: schemas.TransaccionCreate):
    # Validar que la cuenta exista antes de crear la transacción
    if not validar_cuenta(transaccion.cuenta_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La cuenta con ID {transaccion.cuenta_id} no fue encontrada."
        )

    db_transaccion = models.Transaccion(**transaccion.dict())
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def obtener_todas_las_transacciones(db: Session):
    return db.query(models.Transaccion).all()

def obtener_transaccion(db: Session, transaccion_id: int):
    transaccion = db.query(models.Transaccion).filter(models.Transaccion.id == transaccion_id).first()
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con ID {transaccion_id} no fue encontrada."
        )
    return transaccion

def actualizar_transaccion(db: Session, transaccion_id: int, transaccion_data: schemas.TransaccionCreate):
    transaccion = obtener_transaccion(db, transaccion_id)
    for key, value in transaccion_data.dict().items():
        setattr(transaccion, key, value)
    db.commit()
    db.refresh(transaccion)
    return transaccion

def eliminar_transaccion(db: Session, transaccion_id: int):
    transaccion = obtener_transaccion(db, transaccion_id)
    db.delete(transaccion)
    db.commit()