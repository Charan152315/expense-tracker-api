from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import models,schemas,database,auth
from sqlalchemy import func
from datetime import datetime


router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.ExpenseOut)
def create_expense(
    expense:schemas.ExpenseCreate,db:Session=Depends(database.get_db),
    current_user:models.User=Depends(auth.get_current_user)):

    new_expense=models.Expense(**expense.dict(),owner_id=current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.get("/",response_model=list[schemas.ExpenseOut])
def get_expenses(db:Session=Depends(database.get_db),
    current_user:models.User = Depends(auth.get_current_user)):

   expenses = (db.query(models.Expense)
             .filter(models.Expense.owner_id == current_user.id)
             .order_by(models.Expense.created_at.desc())
             .all())

   return expenses

@router.get("/summary")
def get_expense_monthly_summary(db:Session=Depends(database.get_db),current_user:models.User=Depends(auth.get_current_user)):
   
    now=datetime.now()
    start_date=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    end_date=now

    total_amount=db.query(func.sum(models.Expense.amount)).filter(models.Expense.owner_id==current_user.id,
    models.Expense.timestamp>=start_date,models.Expense.timestamp<=end_date).scalar() or 0

    warning=None
    if current_user.monthly_limit and total_amount>current_user.monthly_limit:
       warning=f"You have crossed your monthly limit of {current_user.monthly_limit}"

    category_summary=db.query(models.Expense.category,func.sum(models.Expense.amount).label("total")).filter(
        models.Expense.owner_id==current_user.id).group_by(models.Expense.category).all()

    total_expenses=db.query(models.Expense).filter(models.Expense.owner_id == current_user.id).count()

    category_breakdown={category:float(total) for category,total in category_summary}

    return {
        "total_spent":float(total_amount),
        "by_category":category_breakdown,
        "total_expenses":total_expenses,
        "month":now.strftime("%B %Y"),
        "limit":current_user.monthly_limit,
        "warning":warning,
    }

@router.get("/{id}",response_model=schemas.ExpenseOut)
def get_expense_by_id( id:int,db:Session=Depends(database.get_db),
    current_user:models.User=Depends(auth.get_current_user)):

    expense=db.query(models.Expense).filter(models.Expense.id==id,models.Expense.owner_id==current_user.id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Expense with id {id} not found")

    return expense

@router.put("/{id}", response_model=schemas.ExpenseOut)
def update_expense(id:int,updated_data:schemas.ExpenseCreate,db:Session=Depends(database.get_db),
    current_user:models.User=Depends(auth.get_current_user)):
    
    expense_query=db.query(models.Expense).filter(models.Expense.id==id,models.Expense.owner_id==current_user.id)
    expense=expense_query.first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Expense with id {id} not found")
    
    if (expense.title==updated_data.title and expense.amount == updated_data.amount and expense.category == updated_data.category):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="No changes detected")

    expense_query.update(updated_data.dict(),synchronize_session=False)
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id:int, db:Session=Depends(database.get_db),
    current_user:models.User=Depends(auth.get_current_user)):
   
    expense_query=db.query(models.Expense).filter(models.Expense.id==id,models.Expense.owner_id==current_user.id)
    expense = expense_query.first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Expense with id {id} not found")

    expense_query.delete(synchronize_session=False)
    db.commit()
    return

