from fastapi import APIRouter
from app.utils.migations import run_migrations

router = APIRouter()

@router.get("/run-migrations")
def trigger_migrations():
    try:
        run_migrations()
        return {"message": "Migrations applied successfully!"}
    except Exception as e:
        return {"error": str(e)}
