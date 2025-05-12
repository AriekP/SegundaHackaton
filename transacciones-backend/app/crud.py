# app/crud.py
import random
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

def validar_cuenta(cuenta_id: int) -> bool:
    # Simulación temporal de que las cuentas existen
    # Puedes cambiar esto a una API real cuando tu amigo termine
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