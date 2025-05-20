from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class AccountType(str, enum.Enum):
    AHORRO = "AHORRO"
    CORRIENTE = "CORRIENTE"

class Currency(str, enum.Enum):
    BOB = "BOB"
    USD = "USD"

class AccountStatus(str, enum.Enum):
    ACTIVA = "ACTIVA"
    BLOQUEADA = "BLOQUEADA"

class TransactionType(str, enum.Enum):
    DEPOSITO = "DEPOSITO"
    RETIRO = "RETIRO"
    PAGO = "PAGO"  # Agregado para consistencia con payments_ms

class Account(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    numero_cuenta = Column(String(12), unique=True, index=True, nullable=False)
    saldo = Column(Numeric(10, 2), default=0.00, nullable=False)
    tipo = Column(Enum(AccountType), nullable=False)  # Quitado default para forzar selección
    moneda = Column(Enum(Currency), nullable=False)  # Quitado default para forzar selección
    estado = Column(Enum(AccountStatus), default=AccountStatus.ACTIVA, nullable=False)

    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    tipo = Column(Enum(TransactionType), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(String(100), nullable=True)  # Cambiado a nullable=True
    fecha = Column(DateTime, server_default=func.now(), nullable=False)
    referencia = Column(String(30), nullable=True)  # Cambiado a nullable=True

    account = relationship("Account", back_populates="transactions")