import os
from fastapi import APIRouter
from alembic.config import Config
from alembic import command

router = APIRouter()

@router.get("/run-migrations")
def run_migrations():
    try:
        # Force the absolute path to both alembic.ini and alembic folder
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        alembic_ini = os.path.join(base_path, "alembic.ini")
        alembic_script_location = os.path.join(base_path, "alembic")

        alembic_cfg = Config(alembic_ini)
        alembic_cfg.set_main_option("script_location", alembic_script_location)

        command.upgrade(alembic_cfg, "head")
        return {"message": "Migrations applied successfully!"}
    except Exception as e:
        return {"error": str(e)}
