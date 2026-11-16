from sqlalchemy import text
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import engine
try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        print("Database connected successfully!")
        print("Test result:", result.scalar())

except Exception as e:
    print("Database connection failed!")
    print("Error:", e)