from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import payments, services, auth
from .database import Base, engine

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payments Microservice",
    description="Microservicio para gestión de pagos de servicios",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(services.router, prefix="/services", tags=["services"])