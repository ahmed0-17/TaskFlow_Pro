import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import Base
from app.models import Task

print("Registered tables:", list(Base.metadata.tables.keys()))
print("Task table:", Task.__tablename__)