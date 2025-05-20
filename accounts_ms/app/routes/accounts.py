from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Cuenta no encontrada"}}
)

@router.post("/", response_model=schemas.Account, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    if db.query(models.Account).filter(
        models.Account.numero_cuenta == account.numero_cuenta
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de cuenta ya existe"
        )
    
    db_account = models.Account(
        cliente_id=account.cliente_id,
        numero_cuenta=account.numero_cuenta,
        tipo=account.tipo,
        moneda=account.moneda,
        saldo=0.00
    )
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=list[schemas.Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Account).offset(skip).limit(limit).all()

@router.get("/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    return account

@router.get("/by-number/{account_number}", response_model=schemas.Account)
def read_account_by_number(account_number: str, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(
        models.Account.numero_cuenta == account_number
    ).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    return account

@router.put("/{account_id}", response_model=schemas.Account)
def update_account(
    account_id: int, 
    account_update: schemas.AccountCreate, 
    db: Session = Depends(get_db)
):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cuenta no encontrada"
        )
    
    if account_update.numero_cuenta != db_account.numero_cuenta:
        if db.query(models.Account).filter(
            models.Account.numero_cuenta == account_update.numero_cuenta
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de cuenta ya está en uso"
            )
    
    for field, value in account_update.dict().items():
        setattr(db_account, field, value)
    
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
    
    # No eliminamos transacciones relacionadas
    db.delete(db_account)
    db.commit()
    return None