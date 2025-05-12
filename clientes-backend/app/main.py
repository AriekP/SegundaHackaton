# app/main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.models import cliente
from app.routers import clientes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # o ["*"] si estás en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Montar rutas
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
