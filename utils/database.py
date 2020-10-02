from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configuration import settings

engine = create_engine(
    settings.SQLLITE_DATABASE_URL, connect_args={"check_same_thread": False}
)

# if you want to use MS SQL SERVER, install localdb and set the connection str
# engine = create_engine(settings.SQLSERVER_DATABASE_URL_LOCAL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
