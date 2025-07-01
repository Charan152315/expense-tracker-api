from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    monthly_limit:float

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    monthly_limit:float

    class Config:
        orm_mode=True

class ExpenseBase(BaseModel):
    title:str
    amount:float
    category:str

class ExpenseCreate(ExpenseBase):
    pass            
class ExpenseUpdate(ExpenseBase):
    pass 
class ExpenseOut(ExpenseBase):
    id:int
    owner_id:int
    created_at:datetime

    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token:str
    token_type:str

from pydantic import BaseModel

class TokenData(BaseModel):
    id:int | None=None


class GroupCreate(BaseModel):
    name:str

class GroupOut(BaseModel):
    id:int
    name:str
    owner_id:int
    created_at:datetime
    class Config:
        orm_mode=True           
        