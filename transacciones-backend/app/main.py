# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routers import transacciones

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir las rutas
app.include_router(transacciones.router)

@app.get("/")
def read_root():
    return {"message": "Microservicio de Transacciones Activo"}