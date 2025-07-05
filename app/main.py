from fastapi import FastAPI
from app.database import engine
from app import models
from app.models import Base
import os
from alembic.config import Config
from alembic import command
from app.routes import auth,expense_routes,user_routes,group_routes,run_migrations

#Base.metadata.create_all(bind=engine)

def run_migrations():
    base_path = os.path.abspath(os.path.dirname(__file__))
    alembic_ini = os.path.join(base_path, "alembic.ini")
    alembic_folder = os.path.join(base_path, "alembic")

    config = Config(alembic_ini)
    config.set_main_option("script_location", alembic_folder)
    command.upgrade(config, "head")

run_migrations()

app=FastAPI(title="Expense Tracker API", version="1.0.0")
app.include_router(auth.router)
app.include_router(expense_routes.router)
app.include_router(user_routes.router)
app.include_router(group_routes.router)
app.include_router(run_migrations.router, tags=["Migrations"])


@app.get("/")
def root():
    return {"message": "Expense Tracker API running"}