import os
from alembic.config import Config
from alembic import command

def run_migrations():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini_path = os.path.join(base_dir, "alembic.ini")

    if not os.path.exists(alembic_ini_path):
        raise FileNotFoundError("alembic.ini not found")

    alembic_cfg = Config(alembic_ini_path)
    command.upgrade(alembic_cfg, "head")
