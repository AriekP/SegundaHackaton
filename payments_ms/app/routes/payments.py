from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..payment_processor import process_payment

router = APIRouter()

@router.post("/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    # Verificar que la cuenta existe
    db_account = db.query(models.Account).filter(models.Account.id == payment.cuenta_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    if db_account.estado != "ACTIVA":
        raise HTTPException(status_code=400, detail="Cuenta no está activa")
    
    # Verificar que el proveedor existe
    db_provider = db.query(models.ServiceProvider).filter(models.ServiceProvider.id == payment.proveedor_id).first()
    if not db_provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    if not db_provider.activo:
        raise HTTPException(status_code=400, detail="Proveedor no está activo")
    
    # Verificar fondos suficientes
    if db_account.saldo < payment.monto:
        raise HTTPException(status_code=400, detail="Fondos insuficientes")
    
    # Procesar el pago (simulación)
    payment_result = process_payment(
        provider_code=db_provider.codigo_servicio,
        account_number=db_account.numero_cuenta,
        amount=payment.monto,
        reference=payment.referencia
    )
    
    if not payment_result["success"]:
        raise HTTPException(status_code=400, detail=payment_result["message"])
    
    # Crear el registro de pago
    db_payment = models.Payment(**payment.dict())
    db_payment.estado = "COMPLETADO"
    db_payment.codigo_confirmacion = payment_result["confirmation_code"]
    
    db.add(db_payment)
    
    # Actualizar el saldo de la cuenta
    db_account.saldo -= payment.monto
    
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/{payment_id}", response_model=schemas.Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return db_payment

@router.get("/account/{account_id}", response_model=list[schemas.Payment])
def get_account_payments(account_id: int, db: Session = Depends(get_db)):
    payments = db.query(models.Payment).filter(models.Payment.cuenta_id == account_id).all()
    return payments