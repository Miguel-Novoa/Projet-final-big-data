from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Chaîne de connexion (adapter à votre base)
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydb"

# Crée un moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session locale pour interagir avec la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base commune pour tous les modèles
Base = declarative_base()
