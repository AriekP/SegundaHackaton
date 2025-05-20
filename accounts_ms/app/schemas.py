from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
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

class ServiceType(str, Enum):
    LUZ = "LUZ"
    AGUA = "AGUA"
    GAS = "GAS"
    TELEFONO = "TELEFONO"
    INTERNET = "INTERNET"
    TV = "TV"
    OTROS = "OTROS"

class TransactionType(str, Enum):
    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"
    PAGO = "PAGO"
    TRANSFERENCIA = "TRANSFERENCIA"

# Esquemas para Cuentas
class AccountBase(BaseModel):
    cliente_id: int = Field(..., gt=0, example=1)
    numero_cuenta: str = Field(..., min_length=8, max_length=12, example="12345678")
    tipo: AccountType
    moneda: Currency

    @validator('numero_cuenta')
    def validate_account_number(cls, v):
        if not v.isdigit():
            raise ValueError("El número de cuenta debe contener solo dígitos")
        return v

class AccountCreate(AccountBase):
    saldo: float = Field(0.00, ge=0, example=100.50)

class Account(AccountBase):
    id: int
    saldo: float = Field(..., ge=0)
    estado: AccountStatus = AccountStatus.ACTIVA

    class Config:
        orm_mode = True

class AccountStatusUpdate(BaseModel):
    estado: AccountStatus

# Esquemas para Transacciones
class TransactionBase(BaseModel):
    cuenta_id: int = Field(..., gt=0, example=1)
    monto: float = Field(..., gt=0, example=500.00)
    descripcion: Optional[str] = Field(None, max_length=100, example="Concepto de transacción")
    referencia: Optional[str] = Field(None, max_length=30, example="REF-123456")

class DepositCreate(BaseModel):
    cuenta_id: int = Field(..., gt=0, example=1)
    monto: float = Field(..., gt=0, example=1000.00)
    descripcion: Optional[str] = Field("Depósito de fondos", max_length=100)

class WithdrawCreate(BaseModel):
    cuenta_id: int = Field(..., gt=0, example=1)
    monto: float = Field(..., gt=0, example=500.00)
    descripcion: Optional[str] = Field("Retiro de efectivo", max_length=100)

class PaymentCreate(BaseModel):
    cuenta_id: int = Field(..., gt=0, example=1)
    monto: float = Field(..., gt=0, example=150.00)
    servicio: ServiceType = Field(..., example="LUZ")
    referencia: str = Field(..., min_length=6, max_length=20, example="FACT-123456")

class TransactionCreate(TransactionBase):
    tipo: TransactionType

class Transaction(TransactionBase):
    id: int
    tipo: TransactionType
    fecha: datetime
    cuenta: Optional[Account] = None

    class Config:
        orm_mode = True

# Esquema para respuesta de saldo
class AccountBalance(BaseModel):
    cuenta_id: int
    numero_cuenta: str
    saldo_actual: float
    moneda: Currency
    ultima_actualizacion: datetime

    class Config:
        orm_mode = True

# Esquema para transferencias entre cuentas
class TransferCreate(BaseModel):
    cuenta_origen_id: int = Field(..., gt=0, example=1)
    cuenta_destino_id: int = Field(..., gt=0, example=2)
    monto: float = Field(..., gt=0, example=300.00)
    descripcion: Optional[str] = Field("Transferencia entre cuentas", max_length=100)