import pytest
from app import schemas

def test_create_group(authorized_client):
    res=authorized_client.post("/groups/",json={"name": "Family"})
    assert res.status_code==200
    group=schemas.GroupOut(**res.json())
    assert group.name=="Family"

def test_unauthorized_create_group(client):
    res = client.post("/groups/", json={"name": "Test Group"})
    assert res.status_code==401

def test_get_user_groups(authorized_client):
    res=authorized_client.get("/groups/")
    assert res.status_code==200
    assert isinstance(res.json(),list)

def test_unauthorized_get_groups(client):
    res=client.get("/groups/")
    assert res.status_code==401


def test_add_member_to_group(authorized_client,test_user2,test_group):
    res=authorized_client.post(f"/groups/{test_group['id']}/add_member/{test_user2['id']}")
    assert res.status_code==200
    assert res.json()["message"]==f"User {test_user2['id']} added to group {test_group['id']}"


def test_add_member_already_in_group(authorized_client,test_user,test_group):
    res = authorized_client.post(f"/groups/{test_group['id']}/add_member/{test_user['id']}")
    assert res.status_code==400
    assert res.json()["detail"]=="User already in group"


def test_add_member_group_not_exist(authorized_client,test_user2):
    res = authorized_client.post("/groups/2315/add_member/1")
    assert res.status_code==403

def test_non_owner_add_member(client,test_user2,test_group):
    login=client.post("/login",data={"username":test_user2["email"],"password":test_user2["password"]})
    token=login.json()["access_token"]
    client.headers={"Authorization":f"Bearer {token}"}

    res=client.post(f"/groups/{test_group['id']}/add_member/{test_user2['id']}")
    assert res.status_code==403

def test_list_group_members(authorized_client,test_group):
    res = authorized_client.get(f"/groups/{test_group['id']}/members")
    assert res.status_code==200
    assert isinstance(res.json(),list)


def test_list_members_not_in_group(client,test_user2,test_group):
    login=client.post("/login",data={"username":test_user2["email"],"password":test_user2["password"]})
    token=login.json()["access_token"]
    client.headers={"Authorization":f"Bearer {token}"}
    res = client.get(f"/groups/{test_group['id']}/members")
    assert res.status_code==403


def test_group_expense_summary(authorized_client,test_group):
    res = authorized_client.get(f"/groups/{test_group['id']}/expenses")
    assert res.status_code==200
    assert isinstance(res.json(),list)


def test_group_expense_summary_not_member(client,test_user2,test_group):
    login=client.post("/login",data={"username":test_user2["email"],"password":test_user2["password"]})
    token=login.json()["access_token"]
    client.headers={"Authorization":f"Bearer {token}"}
    res=client.get(f"/groups/{test_group['id']}/expenses")
    assert res.status_code==403
