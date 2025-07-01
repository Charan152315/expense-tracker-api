from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings
from app.main import app
from app import schemas,models
from app.auth import create_access_token
from app.database import get_db
from app.database import Base
import pytest
from datetime import datetime
from alembic import command

DATABASE_URL=f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

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
   
@pytest.fixture
def test_user(client):
    user_data={"email":"charan@23gmail.com","password":"charan15","monthly_limit":5000}
    res =client.post("/users",json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    new_user['monthly_limit'] = user_data['monthly_limit']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data={"email":"charan@2315gmail.com","password":"charan15","monthly_limit":5000}
    res =client.post("/users",json=user_data)
    assert res.status_code==201
    new_user=res.json()
    new_user['password']=user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client,token):
    client.headers={
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_expenses(test_user,session,test_user2):
    expenses_data=[
        {
          "title":"Books",
          "amount":500,
          "category":"Education",
          "owner_id":test_user["id"],
          "created_at":datetime.utcnow()
        },
        {
          "title":"Journey",
          "amount":1200,
          "category":"Travel",
          "owner_id":test_user["id"],
          "created_at":datetime.utcnow()
        },
        {
          "title":"Journey",
          "amount":1200,
          "category":"Travel",
          "owner_id":test_user2["id"],
          "created_at":datetime.utcnow()
        }
]
    expenses = [models.Expense(**exp) for exp in expenses_data]
    session.add_all(expenses)
    session.commit()
    return session.query(models.Expense).all()
    
@pytest.fixture
def test_group(test_user,session):
    group=models.Group(name="Group 1",owner_id=test_user["id"])
    session.add(group)
    session.commit()
    session.refresh(group)

    group_member=models.GroupMember(user_id=test_user["id"],group_id=group.id,role="admin")
    session.add(group_member)
    session.commit()

    return {"id": group.id,"name": group.name,"owner_id": group.owner_id}
