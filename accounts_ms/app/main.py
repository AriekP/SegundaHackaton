from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import accounts, transactions

# Crear tablas en la base de datos (esto es solo para desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Accounts Microservice",
    description="Microservicio para gestión de cuentas bancarias",
    version="1.0.0"
)

# Configurar CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])

@app.get("/")
def read_root():
    return {"message": "Accounts Microservice is running"}