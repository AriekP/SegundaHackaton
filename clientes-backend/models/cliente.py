# app/models/cliente.py
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from datetime import datetime
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20))
    ci = Column(String(20), nullable=False, unique=True)
    fecha_nac = Column(Date)
    direccion = Column(String(255))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
