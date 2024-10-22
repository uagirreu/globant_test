from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# URL de conexión a la base de datos (en este caso a Azure SQL Database)
username = "test"
password = "passUnai1"
server = "serverunai"
database = "unaidb1"

DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}.database.windows.net/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Crear motor de conexión
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función de dependencia
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base para los modelos de SQLAlchemy
Base = declarative_base()