from pydantic import BaseModel, EmailStr

class NotificationEvent(BaseModel):
    order_id: str
    customer_email: EmailStr
    status: str