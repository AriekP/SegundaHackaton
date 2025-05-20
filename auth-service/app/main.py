from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, roles
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    description="Microservicio de autenticación con roles y usuarios",
    version="1.0.0"
)

# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # o ["*"] si estás en desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(roles.router)
