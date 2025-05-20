from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from decimal import Decimal
from typing import List

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Recurso no encontrado"}}
)

@router.post(
    "/deposit",
    response_model=schemas.Transaction,
    status_code=status.HTTP_201_CREATED,
    summary="Realizar un depósito",
    responses={
        400: {"description": "Cuenta inactiva o datos inválidos"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def deposit_funds(deposit: schemas.DepositCreate, db: Session = Depends(get_db)):
    """
    Realiza un depósito en una cuenta.
    
    Requiere:
    - cuenta_id: ID de la cuenta destino
    - monto: Cantidad a depositar (debe ser positivo)
    - descripcion: Concepto del depósito (opcional)
    """
    cuenta = db.query(models.Account).get(deposit.cuenta_id)
    
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cuenta especificada no existe"
        )
    
    if cuenta.estado != "ACTIVA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede depositar en una cuenta inactiva"
        )

    # Crear transacción
    nueva_transaccion = models.Transaction(
        cuenta_id=deposit.cuenta_id,
        tipo="DEPOSITO",
        monto=deposit.monto,
        descripcion=deposit.descripcion or "Depósito de fondos"
    )
    
    # Actualizar saldo
    cuenta.saldo += Decimal(str(deposit.monto))
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    
    return nueva_transaccion

@router.post(
    "/withdraw",
    response_model=schemas.Transaction,
    status_code=status.HTTP_201_CREATED,
    summary="Realizar un retiro",
    responses={
        400: {"description": "Cuenta inactiva, fondos insuficientes o datos inválidos"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def withdraw_funds(withdrawal: schemas.WithdrawCreate, db: Session = Depends(get_db)):
    """
    Realiza un retiro de una cuenta.
    
    Requiere:
    - cuenta_id: ID de la cuenta origen
    - monto: Cantidad a retirar (debe ser positivo y menor al saldo)
    - descripcion: Concepto del retiro (opcional)
    """
    cuenta = db.query(models.Account).get(withdrawal.cuenta_id)
    
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cuenta especificada no existe"
        )
    
    if cuenta.estado != "ACTIVA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede retirar de una cuenta inactiva"
        )
    
    if cuenta.saldo < Decimal(str(withdrawal.monto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar el retiro"
        )

    # Crear transacción
    nueva_transaccion = models.Transaction(
        cuenta_id=withdrawal.cuenta_id,
        tipo="RETIRO",
        monto=withdrawal.monto,
        descripcion=withdrawal.descripcion or "Retiro de fondos"
    )
    
    # Actualizar saldo
    cuenta.saldo -= Decimal(str(withdrawal.monto))
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    
    return nueva_transaccion

@router.post(
    "/payment",
    response_model=schemas.Transaction,
    status_code=status.HTTP_201_CREATED,
    summary="Pagar un servicio",
    responses={
        400: {"description": "Cuenta inactiva, fondos insuficientes o datos inválidos"},
        404: {"description": "Cuenta no encontrada"}
    }
)
def pay_service(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    """
    Realiza el pago de un servicio (luz, agua, etc.).
    
    Requiere:
    - cuenta_id: ID de la cuenta que realiza el pago
    - monto: Cantidad a pagar (debe ser positivo)
    - servicio: Tipo de servicio (LUZ, AGUA, GAS, etc.)
    - referencia: Número de referencia/factura
    """
    cuenta = db.query(models.Account).get(payment.cuenta_id)
    
    if not cuenta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cuenta especificada no existe"
        )
    
    if cuenta.estado != "ACTIVA":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede pagar desde una cuenta inactiva"
        )
    
    if cuenta.saldo < Decimal(str(payment.monto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar el pago"
        )

    # Crear transacción de pago
    nueva_transaccion = models.Transaction(
        cuenta_id=payment.cuenta_id,
        tipo="PAGO",
        monto=payment.monto,
        descripcion=f"Pago de {payment.servicio}",
        referencia=payment.referencia
    )
    
    # Actualizar saldo
    cuenta.saldo -= Decimal(str(payment.monto))
    
    db.add(nueva_transaccion)
    db.commit()
    db.refresh(nueva_transaccion)
    
    return nueva_transaccion

@router.get(
    "/account/{account_id}",
    response_model=List[schemas.Transaction],
    summary="Obtener transacciones de una cuenta"
)
def get_account_transactions(
    account_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene el historial de transacciones de una cuenta específica.
    """
    # Verificar que la cuenta existe
    if not db.query(models.Account).get(account_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cuenta especificada no existe"
        )
    
    return db.query(models.Transaction)\
            .filter(models.Transaction.cuenta_id == account_id)\
            .order_by(models.Transaction.fecha.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

@router.get(
    "/{transaction_id}",
    response_model=schemas.Transaction,
    summary="Obtener detalles de una transacción"
)
def get_transaction_details(transaction_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una transacción específica por su ID.
    """
    transaccion = db.query(models.Transaction).get(transaction_id)
    
    if not transaccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    
    return transaccion