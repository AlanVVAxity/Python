from dataclasses import dataclass
from typing import Literal, NotRequired, TypedDict

TaskStatus = Literal["pending", "in_progress", "completed"]
TaskPriority = Literal["low", "medium", "high"]


class TaskInput(TypedDict):
    title: str
    priority: TaskPriority
    description: NotRequired[str]


class TaskUpdate(TypedDict, total=False):
    title: str
    description: str
    priority: TaskPriority
    status: TaskStatus


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    priority: TaskPriority
    status: TaskStatus = "pending"
    description: str | None = None
