from typing import List
import pytest
from app import schemas

def test_get_all_posts(authorized_client,test_expenses,test_user):
    res=authorized_client.get("/expenses")
    def validate(expense):
        return schemas.ExpenseOut(**expense)
    expenses_list = list(map(validate, res.json()))
    expected_user_expenses = [e for e in test_expenses if e.owner_id == test_user["id"]]
    assert len(res.json())==len(expected_user_expenses)
    assert res.status_code==200

def test_unauthorized_user_get_all_expenses(client,test_expenses):
    res=client.get("/expenses")
    assert res.status_code == 401 

def test_unauthorized_user_get_one_expense(client,test_expenses):
    res=client.get(f"/expenses/{test_expenses[0].id}")
    assert res.status_code == 401        

def test_get_one_expense_not_exist(authorized_client,test_expenses):
        res=authorized_client.get(f"/expenses/2315")
        assert res.status_code==404

def test_get_one_expense(authorized_client,test_expenses):        
     res=authorized_client.get(f"/expenses/{test_expenses[0].id}")
     expense=schemas.ExpenseOut(**res.json())
     assert res.status_code == 200
     assert expense.title==test_expenses[0].title
     assert expense.amount==test_expenses[0].amount
     assert expense.category==test_expenses[0].category
     assert expense.owner_id==test_expenses[0].owner_id
     assert expense.created_at==test_expenses[0].created_at
     
@pytest.mark.parametrize("title,amount,category",[
    ("Books",500,"Education"),
    ("Groceries",1500,"Food"),
    ("Flight Ticket",4000,"Travel"),
    ("Gym",1000,"Fitness"),
])
def test_create_expense(authorized_client,test_expenses,title,amount,category):
    res = authorized_client.post("/expenses",json={"title":title,"amount":amount,"category":category})

    assert res.status_code == 201
    created = schemas.ExpenseOut(**res.json())
    assert created.title == title
    assert created.amount == amount
    assert created.category == category

def test_unauthorized_user_create_expense(client,test_expenses,test_user):
    res=client.post("/expenses",json={"title":"title","amount":"amount","category":"category"})
    assert res.status_code == 401

def test__delete_expense_success(authorized_client,test_expenses,test_user):
    res=authorized_client.delete(f"/expenses/{test_expenses[0].id}")
    assert res.status_code == 204

def test_unauthorized_user_delete_expense(client,test_expenses,test_user):
    res=client.delete(f"/expenses/{test_expenses[0].id}")
    assert res.status_code == 401        

def test_delete_expense_non_exist(authorized_client,test_expenses,test_user):
    res=authorized_client.delete(f"/expenses/2315")
    assert res.status_code == 404

def test_delete_other_users_expense(authorized_client,test_expenses,test_user):
    res=authorized_client.delete(f"/expenses/{test_expenses[2].id}")
    assert res.status_code == 404

def test_update_expense(authorized_client,test_expenses,test_user):
         data = {"title":"Updated Expense","amount":2000,"category":"new update"}
         res = authorized_client.put(f"/expenses/{test_expenses[0].id}",json=data)
         assert res.status_code==200
         updated=schemas.ExpenseOut(**res.json())
         assert updated.title == data["title"]
         assert updated.amount == data["amount"]
         assert updated.category == data["category"]
         assert updated.owner_id == test_user["id"]

def test_update_other_users_expense(authorized_client, test_expenses):
    data = {"title":"Steal","amount":1000,"category":"Grab"}
    res = authorized_client.put(f"/expenses/{test_expenses[2].id}", json=data)
    assert res.status_code == 404

def test_update_expense_unauthorized(client,test_expenses):
    data = {"title":"Unauthorized","amount":1000,"category":"Grab"}
    res = client.put(f"/expenses/{test_expenses[0].id}",json=data)
    assert res.status_code == 401

def test_update_expense_non_exist(authorized_client):
    data = {"title": "Non-existent Expense","amount": 500,"category": "Invalid"}
    res = authorized_client.put("/expenses/2315", json=data)
    assert res.status_code == 404

def test_get_expense_summary(authorized_client, test_expenses, test_user):
    res=authorized_client.get("/expenses/summary")
    assert res.status_code==200
    summary=res.json()
    total_spent=sum(e.amount for e in test_expenses if e.owner_id==test_user["id"])
    by_category={}
    for e in test_expenses:
        if e.owner_id == test_user["id"]:
            if e.category in by_category:
                by_category[e.category] += e.amount
            else:
                by_category[e.category] = e.amount

    assert summary["total_spent"]==float(total_spent)
    assert summary["total_expenses"]==len([e for e in test_expenses if e.owner_id == test_user["id"]])
    assert summary["by_category"]=={k: float(v) for k, v in by_category.items()}
    assert summary["limit"]==test_user["monthly_limit"]

    if total_spent>test_user["monthly_limit"]:
        assert summary["warning"] is not None
    else:
        assert summary["warning"] is None
    assert isinstance(summary["month"], str)

def test_unauthorized_user_get_expense_summary(client):
    res=client.get("/expenses/summary")
    assert res.status_code==401
