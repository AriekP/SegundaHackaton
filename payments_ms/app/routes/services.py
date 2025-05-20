from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.post("/providers", response_model=schemas.ServiceProvider)
def create_service_provider(
    provider: schemas.ServiceProviderCreate, 
    db: Session = Depends(get_db)
):
    # Verificar si el código de servicio ya existe
    db_provider = db.query(models.ServiceProvider).filter(
        models.ServiceProvider.codigo_servicio == provider.codigo_servicio
    ).first()
    
    if db_provider:
        raise HTTPException(status_code=400, detail="Código de servicio ya existe")
    
    db_provider = models.ServiceProvider(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

@router.get("/providers", response_model=list[schemas.ServiceProvider])
def read_service_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    providers = db.query(models.ServiceProvider).offset(skip).limit(limit).all()
    return providers

@router.get("/providers/{provider_id}", response_model=schemas.ServiceProvider)
def read_service_provider(provider_id: int, db: Session = Depends(get_db)):
    db_provider = db.query(models.ServiceProvider).filter(models.ServiceProvider.id == provider_id).first()
    if not db_provider:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return db_provider

@router.get("/providers/by-type/{service_type}", response_model=list[schemas.ServiceProvider])
def read_service_providers_by_type(service_type: schemas.ServiceType, db: Session = Depends(get_db)):
    providers = db.query(models.ServiceProvider).filter(
        models.ServiceProvider.tipo_servicio == service_type
    ).all()
    return providers