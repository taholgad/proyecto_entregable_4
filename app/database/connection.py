"""
Configuración de la conexión a MySQL con SQLAlchemy
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Parámetros de conexión
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "task_manager")

# URL de conexión MySQL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Crear engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Para ver las queries SQL en desarrollo
    pool_pre_ping=True,  # Verificar conexión antes de usar
)

# Crear SessionLocal para obtener sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """
    Dependencia para obtener sesión de base de datos en FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
