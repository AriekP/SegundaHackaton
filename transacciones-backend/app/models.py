# app/models.py
from sqlalchemy import Column, Integer, DECIMAL, DateTime, String, Enum, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, nullable=False)  # Solo usa el ID de la cuenta
    tipo = Column(Enum("DEPOSITO", "RETIRO", "PAGO_SERVICIO", "TRANSFERENCIA"), nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    descripcion = Column(String(100))
    fecha = Column(DateTime, default=datetime.utcnow)
    referencia = Column(String(30))