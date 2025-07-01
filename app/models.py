from sqlalchemy import Boolean,Integer,String,Float,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import Column, DateTime, func

class User(Base):
    __tablename__="users"

    id =Column(Integer,primary_key=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password= Column(String,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    monthly_limit=Column(Float,nullable=False,server_default="0")
    expenses=relationship("Expense",back_populates="owner")

class Expense(Base):
    __tablename__="expenses"

    id = Column(Integer,primary_key=True,nullable=False)
    title= Column(String,nullable=False)
    amount= Column(Float,nullable=False)
    category=Column(String,nullable=True)
    timestamp=Column(TIMESTAMP(timezone=True),server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    group_id=Column(Integer,ForeignKey("groups.id"),nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner=relationship("User",back_populates="expenses")
    group=relationship("Group",back_populates="expenses")

class Group(Base):
    __tablename__="groups"

    id =Column(Integer,primary_key=True,nullable=False)
    name= Column(String,nullable=False)
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),server_default=text('now()'))

    members=relationship("GroupMember",back_populates="group")
    expenses=relationship("Expense",back_populates="group")

class GroupMember(Base):
    __tablename__="group_members"

    id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    group_id=Column(Integer,ForeignKey("groups.id"),nullable=False)
    role=Column(String,default="member")

    group=relationship("Group",back_populates="members")

        