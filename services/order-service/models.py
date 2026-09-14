from sqlalchemy import Column, String
from database import Base
import uuid

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    idempotency_key = Column(String, unique=True, index=True, nullable=False)