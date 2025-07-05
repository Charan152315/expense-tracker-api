from fastapi import APIRouter
from alembic.config import Config
from alembic import command

router = APIRouter()

@router.get("/run-migrations")
def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        return {"message": "Migrations applied successfully!"}
    except Exception as e:
        return {"error": str(e)}
