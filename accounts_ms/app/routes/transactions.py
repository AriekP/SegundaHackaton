from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from decimal import Decimal

router = APIRouter()

@router.post("/deposit", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def deposit_funds(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Verificar que la cuenta existe
    db_account = db.query(models.Account).filter(
        models.Account.id == transaction.cuenta_id
    ).first()
    
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    
    if db_account.estado != models.AccountStatus.ACTIVA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cuenta no está activa"
        )
    
    # Crear la transacción
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    
    # Actualizar el saldo de la cuenta
    db_account.saldo += Decimal(str(transaction.monto))
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.post("/withdraw", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def withdraw_funds(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    # Verificar que la cuenta existe
    db_account = db.query(models.Account).filter(
        models.Account.id == transaction.cuenta_id
    ).first()
    
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    
    if db_account.estado != models.AccountStatus.ACTIVA:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La cuenta no está activa"
        )
    
    # Verificar fondos suficientes
    if db_account.saldo < Decimal(str(transaction.monto)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fondos insuficientes"
        )
    
    # Crear la transacción
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    
    # Actualizar el saldo de la cuenta
    db_account.saldo -= Decimal(str(transaction.monto))
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/account/{account_id}", response_model=list[schemas.Transaction])
def get_account_transactions(account_id: int, db: Session = Depends(get_db)):
    # Verificar que la cuenta existe
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    
    transactions = db.query(models.Transaction).filter(
        models.Transaction.cuenta_id == account_id
    ).order_by(models.Transaction.fecha.desc()).all()
    
    return transactions

@router.get("/", response_model=list[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id
    ).first()
    
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    
    return db_transaction