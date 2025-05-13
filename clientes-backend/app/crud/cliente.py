# app/crud/cliente.py
from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCrear, ClienteActualizar

def crear_cliente(db: Session, datos: ClienteCrear):
    nuevo = Cliente(**datos.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar_clientes(db: Session):
    return db.query(Cliente).filter(Cliente.activo == True).all()

def obtener_cliente(db: Session, cliente_id: int):
    return db.query(Cliente).get(cliente_id)

def actualizar_cliente(db: Session, cliente_id: int, datos: ClienteActualizar):
    cliente = db.query(Cliente).get(cliente_id)
    if cliente:
        for key, value in datos.dict().items():
            setattr(cliente, key, value)
        db.commit()
    return cliente

def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).get(cliente_id)
    if cliente:
        cliente.activo = False
        db.commit()
    return cliente
