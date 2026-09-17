import json
import os
import boto3
from fastapi import FastAPI, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from confluent_kafka import Producer

import models
from database import engine, get_db
from schemas import OrderCreate

app = FastAPI(title="Order Service")

# --- ROUTAGE CLOUD-NATIVE (LOCAL vs PROD) ---
ENV = os.getenv("ENVIRONMENT", "local")

if ENV == "production":
    print("🚀 Démarrage en mode AWS CLOUD (SQS)")
    SQS_URL = os.getenv("AWS_SQS_ORDER_EVENTS_URL")
    # L'authentification (clés) sera gérée automatiquement par le rôle IAM du cluster EKS
    sqs_client = boto3.client('sqs', region_name='eu-west-3')
    
    def send_event(order_id, payload):
        try:
            sqs_client.send_message(
                QueueUrl=SQS_URL, 
                MessageBody=json.dumps(payload)
            )
            print(f"Événement envoyé à AWS SQS: {order_id}")
        except Exception as e:
            print(f"Erreur AWS SQS: {e}")

else:
    print("💻 Démarrage en mode LOCAL (Kafka)")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    KAFKA_TOPIC = "order-events"
    producer = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})

    def delivery_report(err, msg):
        if err is not None:
            print(f"Erreur Kafka : {err}")
        else:
            print(f"Événement Kafka publié [Partition: {msg.partition()}]")

    def send_event(order_id, payload):
        try:
            producer.produce(
                KAFKA_TOPIC, 
                key=str(order_id), 
                value=json.dumps(payload),
                callback=delivery_report
            )
            producer.poll(0)
        except Exception as e:
            print(f"Erreur Kafka: {e}")

# --- API ENDPOINTS ---
@app.post("/api/orders", status_code=202)
async def create_order(
    order: OrderCreate, 
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
    db: Session = Depends(get_db)
):
    db_order = models.Order(
        customer_id=order.customer_id,
        idempotency_key=idempotency_key,
        status="PENDING"
    )
    
    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Idempotency-Key existe déjà.")

    event_payload = {
        "order_id": str(db_order.id),
        "customer_id": db_order.customer_id,
        "items": [{"product_id": item.product_id, "quantity": item.quantity} for item in order.items],
        "status": db_order.status
    }
    
    # Appel de la fonction agnostique (elle se débrouille selon l'environnement)
    send_event(db_order.id, event_payload)

    return {
        "message": "Order saved and event published",
        "order_id": db_order.id,
        "status": db_order.status
    }