import json
import os
import threading
from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaError

app = FastAPI(title="Inventory Service")

# --- CONFIGURATION KAFKA ---
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = "order-events"
KAFKA_GROUP_ID = "inventory-group"

def consume_messages():
    """ Fonction qui tourne en boucle pour écouter les nouveaux messages """
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'group.id': KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest' # Lit les messages depuis le début si nouveau groupe
    })
    consumer.subscribe([KAFKA_TOPIC])

    # FORCING DOCKER UPDATE
    print("🚀 [INVENTORY] Démarrage du Consumer Kafka...", flush=True)
    
    while True:
        msg = consumer.poll(1.0) # Attend un message pendant 1 seconde
        
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"❌ Erreur Kafka: {msg.error()}")
                break

        # Message reçu avec succès !
        try:
            event_data = json.loads(msg.value().decode('utf-8'))
            order_id = event_data.get("order_id")
            items = event_data.get("items", [])
            
            # ---> AJOUTE FLUSH=TRUE SUR CES DEUX LIGNES <---
            print(f"📦 [INVENTORY] Événement reçu pour la commande {order_id} !", flush=True)
            print(f"   -> Vérification et déduction des stocks pour : {items}", flush=True)
            
        except Exception as e:
            print(f"⚠️ Erreur de traitement du message: {e}", flush=True)

# Au démarrage de l'API FastAPI, on lance le Consumer Kafka en arrière-plan
@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=consume_messages, daemon=True)
    thread.start()

@app.get("/")
def read_root():
    return {"message": "Inventory Service is running and listening to Kafka"}