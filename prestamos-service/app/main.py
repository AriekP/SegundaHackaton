from fastapi import FastAPI
from app.database import Base, engine
from app.routers import prestamos
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

Base.metadata.create_all(bind=engine)
app.include_router(prestamos.router)
# Incluye el router con prefijo
app.include_router(prestamos.router, prefix="/prestamos", tags=["prestamos"])