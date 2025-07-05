import os
from fastapi import APIRouter, HTTPException
from alembic.config import Config
from alembic import command

router = APIRouter()

@router.get("/run-migrations")
def run_migrations():
    try:
        base_path = os.getcwd()
        alembic_ini = os.path.join(base_path, "alembic.ini")
        alembic_script_location = os.path.join(base_path, "alembic")

        print(f"alembic_ini = {alembic_ini}")
        print(f"alembic_script_location = {alembic_script_location}")
        print(f"os.getcwd() = {os.getcwd()}")

        alembic_cfg = Config(alembic_ini)
        alembic_cfg.set_main_option("script_location", alembic_script_location)

        command.upgrade(alembic_cfg, "head")
        return {"message": "Migrations applied successfully!"}
    except Exception as e:
        return {"error": str(e)}
