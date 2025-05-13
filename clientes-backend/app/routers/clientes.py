# app/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.cliente import ClienteCrear, ClienteActualizar, ClienteOut
from app.crud import cliente as crud_cliente

router = APIRouter()

@router.post("/", response_model=ClienteOut)
def crear_cliente(cliente: ClienteCrear, db: Session = Depends(get_db)):
    return crud_cliente.crear_cliente(db, cliente)

@router.get("/", response_model=list[ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    return crud_cliente.listar_clientes(db)

@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = crud_cliente.obtener_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{cliente_id}", response_model=ClienteOut)
def actualizar_cliente(cliente_id: int, datos: ClienteActualizar, db: Session = Depends(get_db)):
    return crud_cliente.actualizar_cliente(db, cliente_id, datos)

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return crud_cliente.eliminar_cliente(db, cliente_id)
