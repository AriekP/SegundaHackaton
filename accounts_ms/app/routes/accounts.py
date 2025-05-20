from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={
        404: {"description": "Cuenta no encontrada"},
        400: {"description": "Solicitud inválida"}
    }
)

@router.post(
    "/",
    response_model=schemas.Account,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Número de cuenta ya existe o datos inválidos"},
        422: {"description": "Error de validación de datos"}
    }
)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva cuenta bancaria.
    - **cliente_id**: ID del cliente (requerido)
    - **numero_cuenta**: Número único de cuenta (8-12 dígitos, requerido)
    - **tipo**: Tipo de cuenta (AHORRO/CORRIENTE, requerido)
    - **moneda**: Moneda de la cuenta (BOB/USD, requerido)
    - **saldo**: Saldo inicial (opcional, default=0)
    """
    # Verificar unicidad del número de cuenta
    if db.query(models.Account).filter_by(numero_cuenta=account.numero_cuenta).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de cuenta ya está registrado"
        )

    # Crear la cuenta
    db_account = models.Account(
        cliente_id=account.cliente_id,
        numero_cuenta=account.numero_cuenta,
        tipo=account.tipo,
        moneda=account.moneda,
        saldo=account.saldo if account.saldo is not None else 0.00
    )
    
    try:
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la cuenta: {str(e)}"
        )

@router.get(
    "/",
    response_model=List[schemas.Account],
    summary="Listar cuentas",
    description="Obtiene un listado de cuentas con opción de filtrado por cliente_id"
)
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    cliente_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Account)
    
    if cliente_id is not None:
        query = query.filter(models.Account.cliente_id == cliente_id)
    
    return query.offset(skip).limit(limit).all()

@router.get(
    "/{account_id}",
    response_model=schemas.Account,
    responses={404: {"description": "Cuenta no encontrada"}}
)
def read_account(account_id: int, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una cuenta específica por su ID.
    """
    account = db.query(models.Account).get(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {account_id} no encontrada"
        )
    return account

@router.get(
    "/by-number/{account_number}",
    response_model=schemas.Account,
    responses={
        404: {"description": "Cuenta no encontrada"},
        400: {"description": "Formato de número de cuenta inválido"}
    }
)
def read_account_by_number(account_number: str, db: Session = Depends(get_db)):
    """
    Busca una cuenta por su número de cuenta.
    - El número debe contener entre 8-12 dígitos
    """
    if not account_number.isdigit() or len(account_number) < 8 or len(account_number) > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de cuenta debe contener entre 8-12 dígitos"
        )
    
    account = db.query(models.Account).filter_by(numero_cuenta=account_number).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con número {account_number} no encontrada"
        )
    return account

@router.put(
    "/{account_id}",
    response_model=schemas.Account,
    responses={
        404: {"description": "Cuenta no encontrada"},
        400: {"description": "Número de cuenta ya en uso o datos inválidos"}
    }
)
def update_account(
    account_id: int,
    account_update: schemas.AccountCreate,
    db: Session = Depends(get_db)
):
    """
    Actualiza todos los campos de una cuenta.
    """
    db_account = db.query(models.Account).get(account_id)
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {account_id} no encontrada"
        )
    
    # Validar unicidad si cambia el número de cuenta
    if account_update.numero_cuenta != db_account.numero_cuenta:
        if db.query(models.Account).filter_by(numero_cuenta=account_update.numero_cuenta).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo número de cuenta ya está en uso"
            )
    
    try:
        for field, value in account_update.dict(exclude_unset=True).items():
            setattr(db_account, field, value)
        
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la cuenta: {str(e)}"
        )

@router.patch(
    "/{account_id}/status",
    response_model=schemas.Account,
    responses={
        404: {"description": "Cuenta no encontrada"},
        400: {"description": "Estado inválido"}
    }
)
def update_account_status(
    account_id: int,
    status_update: schemas.AccountStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza solo el estado de una cuenta (ACTIVA/BLOQUEADA).
    """
    db_account = db.query(models.Account).get(account_id)
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {account_id} no encontrada"
        )
    
    try:
        db_account.estado = status_update.estado
        db.commit()
        db.refresh(db_account)
        return db_account
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el estado: {str(e)}"
        )

@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"description": "Cuenta no encontrada"},
        400: {"description": "La cuenta tiene saldo distinto de cero"}
    }
)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    """
    Elimina una cuenta (solo si tiene saldo cero).
    """
    db_account = db.query(models.Account).get(account_id)
    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cuenta con ID {account_id} no encontrada"
        )
    
    if db_account.saldo != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar una cuenta con saldo distinto de cero"
        )
    
    try:
        db.delete(db_account)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la cuenta: {str(e)}"
        )