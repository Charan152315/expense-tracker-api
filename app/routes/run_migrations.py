import os
from fastapi import APIRouter
from alembic.config import Config
from alembic import command

router = APIRouter()

@router.get("/run-migrations")
def run_migrations():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        alembic_ini_path = os.path.join(base_dir, "alembic.ini")
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("script_location", "alembic")
        command.upgrade(alembic_cfg, "head")
        return {"message": "Migrations applied successfully!"}
    except Exception as e:
        return {"error": str(e)}
