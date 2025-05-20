from sqlalchemy import Column, Integer, String, Numeric, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base
import enum

class ServiceType(str, enum.Enum):
    LUZ = "LUZ"
    AGUA = "AGUA"
    GAS = "GAS"
    TELEFONO = "TELEFONO"
    INTERNET = "INTERNET"
    TV = "TV"
    OTROS = "OTROS"

class PaymentStatus(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    COMPLETADO = "COMPLETADO"
    FALLIDO = "FALLIDO"

class ServiceProvider(Base):
    __tablename__ = "proveedores_servicio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    tipo_servicio = Column(Enum(ServiceType), nullable=False)
    codigo_servicio = Column(String(20), unique=True, nullable=False)
    activo = Column(Boolean, default=True)

class Payment(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas.id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedores_servicio.id"), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    referencia = Column(String(30), nullable=False)
    fecha = Column(DateTime, server_default=func.now())
    estado = Column(Enum(PaymentStatus), default=PaymentStatus.PENDIENTE)
    codigo_confirmacion = Column(String(50))