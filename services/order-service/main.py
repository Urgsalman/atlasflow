from fastapi import FastAPI, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated

import models
from database import engine, get_db
from schemas import OrderCreate


app = FastAPI(title="Order Service")

@app.post("/api/orders", status_code=202)
async def create_order(
    order: OrderCreate, 
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    db: Session = Depends(get_db)
):
    # 1. Créer l'objet base de données
    db_order = models.Order(
        customer_id=order.customer_id,
        idempotency_key=idempotency_key,
        status="PENDING"
    )
    
    # 2. Sauvegarder dans PostgreSQL avec gestion de l'idempotence
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except IntegrityError:
        db.rollback()
        # Si l'idempotency_key existe déjà, la contrainte 'unique=True' lève une erreur
        raise HTTPException(
            status_code=409, 
            detail="Une commande avec cette Idempotency-Key existe déjà."
        )

    return {
        "message": "Order saved to database",
        "order_id": db_order.id,
        "status": db_order.status
    }