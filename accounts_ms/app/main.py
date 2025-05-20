from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import accounts, transactions

# Crear tablas en la base de datos (esto es solo para desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Accounts Microservice",
    description="Microservicio para gestión de cuentas bancarias",  # Corregí "cuentas" -> "cuentas"
    version="1.0.0",
    docs_url="/docs",  # Explicitamente define la ruta de docs
    redoc_url="/redoc"  # Explicitamente define la ruta de redoc
)

# Configurar CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplaza con tus dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Especifica métodos en lugar de "*"
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Accounts Microservice is running now"}