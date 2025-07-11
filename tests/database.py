from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.main import app
from app import schemas
from app.database import get_db
from app.database import Base
import pytest
from alembic import command

DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.test_database_name}"

engine=create_engine(DATABASE_URL)
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

@pytest.fixture(scope="function")
def session():
   Base.metadata.drop_all(bind=engine)
   Base.metadata.create_all(bind=engine)
   #command.upgrade("head")
   #command.downgrade("base")
   db=TestingSessionLocal()
   try:
        yield db
   finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
   def override_get_db():
    try:
        yield session
    finally:
        session.close()
   app.dependency_overrides[get_db]=override_get_db         
   yield TestClient(app)
   