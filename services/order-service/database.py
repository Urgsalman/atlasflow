from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# On lit l'URL depuis une variable d'environnement, avec un fallback pour le dev local manuel
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://atlas_user:atlas_password@localhost:5432/atlas_orders"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()