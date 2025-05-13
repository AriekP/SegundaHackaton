# app/schemas/cliente.py
from pydantic import BaseModel, EmailStr
from datetime import date

class ClienteBase(BaseModel):
    nombre: str
    correo: EmailStr
    telefono: str | None = None
    ci: str
    fecha_nac: date
    direccion: str | None = None

class ClienteCrear(ClienteBase):
    pass

class ClienteActualizar(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int
    activo: bool

    class Config:
        orm_mode = True
