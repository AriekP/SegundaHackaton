from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    # Verificar si el número de cuenta ya existe
    db_account = db.query(models.Account).filter(
        models.Account.numero_cuenta == account.numero_cuenta
    ).first()
    
    if db_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de cuenta ya existe"
        )
    
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=list[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = db.query(models.Account).offset(skip).limit(limit).all()
    return accounts

@router.get("/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    return db_account

@router.get("/by-number/{account_number}", response_model=schemas.Account)
def read_account_by_number(account_number: str, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(
        models.Account.numero_cuenta == account_number
    ).first()
    
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    return db_account

@router.put("/{account_id}", response_model=schemas.Account)
def update_account(
    account_id: int, 
    account: schemas.AccountCreate, 
    db: Session = Depends(get_db)
):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    
    # Verificar si el nuevo número de cuenta ya existe (si ha cambiado)
    if account.numero_cuenta != db_account.numero_cuenta:
        existing_account = db.query(models.Account).filter(
            models.Account.numero_cuenta == account.numero_cuenta
        ).first()
        
        if existing_account:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de cuenta ya está en uso"
            )
    
    # Actualizar los campos
    for key, value in account.dict().items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    
    db.delete(db_account)
    db.commit()
    return None