from app import schemas
import pytest
from jose import jwt
from app.config import settings

#def test_root(client):
#    res=client.get("/")
#   print(res.json().get('message'))
#    assert res.json().get('message')== "Expense Tracker API running"
#    assert res.status_code == 200


def test_create_user(client):
    res=client.post(
        "/users",json={"email":"deepa231@gmail.com","password":"charan23","monthly_limit":5000})
    new_user=schemas.UserOut(**res.json())
    assert new_user.email=="deepa231@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user,client):
    res=client.post(
        "/login",data={"username":test_user['email'],"password":test_user['password']})
    login_res=schemas.Token(**res.json())
    payload=jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id=payload.get("user_id")
    assert id==test_user['id']
    assert login_res.token_type=="bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email,password,status_code,error_detail",[
    ("charan@23gmail.com","wrongpass",403,"Invalid Credentials"),
    ("wrong@gmail.com","charan15",403,"Invalid Credentials"),
    ("wrong@gmail.com","wrongpass",403,"Invalid Credentials"),
    ("","password23",403,"Invalid Credentials"),
    ("charan@gmail.com","",403,"Invalid Credentials")
])
def test_incorrect_login(email,password,status_code,error_detail,client,test_user):
    res = client.post("/login",data={"username": email,"password": password})
    assert res.status_code == status_code
    assert res.json()["detail"] == error_detail

def test_duplicate_user_creation(client,test_user):
    res = client.post("/users",json={"email":test_user["email"],"password":"newpass","monthly_limit":3000})
    assert res.status_code==406
    assert res.json()["detail"] == "Email was already registered"  

def test_create_user_missing_fields(client):
    res = client.post("/users", json={"email":"test@gmail.com"})
    assert res.status_code==422  
