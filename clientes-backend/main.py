# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.models import cliente
from app.routers import clientes

app = FastAPI()

# Crear tablas
Base.metadata.create_all(bind=engine)

# Montar rutas
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
