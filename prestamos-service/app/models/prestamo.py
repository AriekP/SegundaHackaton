from sqlalchemy import Column, Integer, Float, String, Date
from datetime import date
from app.database import Base

class Prestamo(Base):
    __tablename__ = "prestamos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    monto = Column(Float, nullable=False)
    interes = Column(Float, nullable=False)
    plazo_meses = Column(Integer, nullable=False)
    tipo = Column(String(50), default="consumo")
    fecha_solicitud = Column(Date, default=date.today)
    estado = Column(String(20), default="pendiente")
    observaciones = Column(String(255), nullable=True)
