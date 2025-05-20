# app/models/user.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    correo = Column(String(100), unique=True, nullable=False)         # ✔ longitud definida
    hashed_password = Column(String(255), nullable=False)             # ✅ longitud añadida
    cliente_id = Column(Integer, nullable=True)

    roles = relationship("UsuarioRol", back_populates="usuario")
