from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    correo: EmailStr
    cliente_id: Optional[int] = None

class UsuarioCrear(UsuarioBase):
    password: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
