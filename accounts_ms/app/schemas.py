from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class AccountType(str, Enum):
    AHORRO = "AHORRO"
    CORRIENTE = "CORRIENTE"

class Currency(str, Enum):
    BOB = "BOB"
    USD = "USD"

class AccountStatus(str, Enum):
    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"

class TransactionType(str, Enum):
    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"

# Esquemas para Cuentas
class AccountBase(BaseModel):
    cliente_id: int = Field(..., example=1)
    numero_cuenta: str = Field(..., min_length=10, max_length=12, example="1234567890")
    saldo: float = Field(0.00, ge=0, example=1000.50)
    tipo: AccountType = AccountType.AHORRO
    moneda: Currency = Currency.BOB
    estado: AccountStatus = AccountStatus.ACTIVA

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True

# Esquemas para Transacciones
class TransactionBase(BaseModel):
    cuenta_id: int = Field(..., example=1)
    tipo: TransactionType
    monto: float = Field(..., gt=0, example=500.00)
    descripcion: Optional[str] = Field(None, example="Depósito inicial")
    referencia: Optional[str] = Field(None, example="DEP-001")

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True