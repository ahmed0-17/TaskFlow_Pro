from pydantic import BaseModel, Field
from enum import Enum
from pydantic import ConfigDict
from datetime import datetime

class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCategory(str, Enum):
    WORK = "Work"
    PERSONAL = "Personal"
    STUDY = "Study"
    SHOPPING = "Shopping"





class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    priority: TaskPriority = TaskPriority.MEDIUM

    category: TaskCategory    



class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: str | None = None

    priority: TaskPriority | None = None

    category: TaskCategory | None = None

    is_completed: bool | None = None




class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    is_completed: bool
    priority: TaskPriority
    category: TaskCategory
    created_at: datetime