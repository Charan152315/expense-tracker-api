from fastapi import FastAPI
from app.database import engine
from app import models
from app.models import Base
import os
from app.routes import auth,expense_routes,user_routes,group_routes,run_migrations

#Base.metadata.create_all(bind=engine)


app=FastAPI(title="Expense Tracker API", version="1.0.0")
app.include_router(auth.router)
app.include_router(expense_routes.router)
app.include_router(user_routes.router)
app.include_router(group_routes.router)
app.include_router(run_migrations.router, tags=["Migrations"])


@app.get("/")
def root():
    return {"message": "Expense Tracker API running"}