import json
import os
import threading
from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaError

app = FastAPI(title="Notification Service")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = "order-events"
KAFKA_GROUP_ID = "notification-group" # <-- GROUPE DIFFÉRENT ICI

def consume_messages():
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([KAFKA_TOPIC])

    print("📧 [NOTIFICATION] Démarrage du Consumer Kafka...", flush=True)
    
    while True:
        msg = consumer.poll(1.0)
        if msg is None: continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                print(f"❌ Erreur Kafka: {msg.error()}", flush=True)
                break
            continue

        try:
            event_data = json.loads(msg.value().decode('utf-8'))
            order_id = event_data.get("order_id")
            customer_id = event_data.get("customer_id")
            
            print(f"📩 [NOTIFICATION] Événement reçu ! Simulation d'email pour la commande {order_id}...", flush=True)
            print(f"   -> 'Bonjour client {customer_id}, votre commande est confirmée !'", flush=True)
        except Exception as e:
            print(f"⚠️ Erreur: {e}", flush=True)

@app.on_event("startup")
def startup_event():
    threading.Thread(target=consume_messages, daemon=True).start()

@app.get("/")
def read_root():
    return {"message": "Notification Service is running"}