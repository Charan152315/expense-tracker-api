from fastapi import APIRouter
from alembic.config import Config
from alembic import command
import os

router = APIRouter()

@router.get("/run-migrations")
def run_migrations():
    try:
        alembic_ini_path = os.path.abspath("alembic.ini")
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", "alembic") 
        command.upgrade(alembic_cfg, "head")
        return {"message": "Migrations applied successfully!"}
    except Exception as e:
        return {"error": str(e)}

