from app.core.database import Base
from app.models import Task, User


def test_models_registered():
    assert "tasks" in Base.metadata.tables
    assert "users" in Base.metadata.tables


def test_task_table_name():
    assert Task.__tablename__ == "tasks"


def test_user_table_name():
    assert User.__tablename__ == "users"