from fastapi import FastAPI
from schemas import NotificationEvent
import logging

app = FastAPI(title="Notification Service")
logging.basicConfig(level=logging.INFO)

@app.post("/api/notifications")
async def send_notification(event: NotificationEvent):
    # Ici on simulera l'envoi d'un email ou SMS
    logging.info(f"Simulation d'envoi email à {event.customer_email} pour la commande {event.order_id}. Statut: {event.status}")
    return {"message": "Notification process triggered", "success": True}