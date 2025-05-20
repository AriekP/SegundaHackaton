from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class ServiceType(str, Enum):
    LUZ = "LUZ"
    AGUA = "AGUA"
    GAS = "GAS"
    TELEFONO = "TELEFONO"
    INTERNET = "INTERNET"
    TV = "TV"
    OTROS = "OTROS"

class PaymentStatus(str, Enum):
    PENDIENTE = "PENDIENTE"
    COMPLETADO = "COMPLETADO"
    FALLIDO = "FALLIDO"

class ServiceProviderBase(BaseModel):
    nombre: str
    tipo_servicio: ServiceType
    codigo_servicio: str
    activo: bool = True

class ServiceProviderCreate(ServiceProviderBase):
    pass

class ServiceProvider(ServiceProviderBase):
    id: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    cuenta_id: int
    proveedor_id: int
    monto: float
    referencia: str
    estado: Optional[PaymentStatus] = PaymentStatus.PENDIENTE
    codigo_confirmacion: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True