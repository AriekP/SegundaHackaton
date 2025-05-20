from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransaccionBase(BaseModel):
    cuenta_id: int
    tipo: str
    monto: float
    descripcion: Optional[str] = None
    referencia: Optional[str] = None

class TransaccionCreate(TransaccionBase):
    pass

class TransaccionResponse(TransaccionBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True