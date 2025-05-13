from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey, DateTime
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

class Account(Base):
    __tablename__ = "cuentas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)  # Sin FK por simplicidad en MVP
    numero_cuenta = Column(String(12), unique=True, index=True)
    saldo = Column(Numeric(10, 2), default=0.00)
    tipo = Column(Enum(AccountType), default=AccountType.AHORRO)
    moneda = Column(Enum(Currency), default=Currency.BOB)
    estado = Column(Enum(AccountStatus), default=AccountStatus.ACTIVA)

    def __repr__(self):
        return f"<Account {self.numero_cuenta}>"

class Transaction(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    tipo = Column(Enum(TransactionType), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(String(100))
    fecha = Column(DateTime, server_default=func.now())
    referencia = Column(String(30))

    def __repr__(self):
        return f"<Transaction {self.id} - {self.tipo}>"