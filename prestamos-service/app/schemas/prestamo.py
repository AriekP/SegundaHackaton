from pydantic import BaseModel, Field
from datetime import date

class PrestamoBase(BaseModel):
    cliente_id: int
    monto: float
    interes: float
    plazo_meses: int
    tipo: str = "consumo"
    fecha_solicitud: date = Field(default_factory=date.today)
    estado: str = "pendiente"
    observaciones: str | None = None

class PrestamoCreate(PrestamoBase):
    pass

class PrestamoOut(PrestamoBase):
    id: int

    class Config:
        from_attributes = True
