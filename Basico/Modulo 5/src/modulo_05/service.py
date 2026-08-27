from dataclasses import replace

from modulo_05.models import Task, TaskInput, TaskStatus, TaskUpdate
from modulo_05.repository import TaskRepository


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, task: Task) -> Task:
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def list_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise KeyError(f"La tarea con id {task.id} no existe.")

        self._tasks[task.id] = task
        return task

    def get_next_id(self) -> int:
        next_id = self._next_id
        self._next_id += 1
        return next_id


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create_task(self, data: TaskInput) -> Task:
        if not data["title"].strip():
            raise ValueError("El título no puede estar vacío.")

        if not isinstance(self._repository, InMemoryTaskRepository):
            raise TypeError("Este ejercicio requiere InMemoryTaskRepository.")

        task = Task(
            id=self._repository.get_next_id(),
            title=data["title"].strip(),
            priority=data["priority"],
            description=data.get("description"),
        )

        return self._repository.add(task)

    def get_task(self, task_id: int) -> Task | None:
        return self._repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self._repository.list_all()

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        current_task = self._repository.get_by_id(task_id)

        if current_task is None:
            raise KeyError(f"La tarea con id {task_id} no existe.")

        title = data.get("title", current_task.title).strip()

        if not title:
            raise ValueError("El título no puede estar vacío.")

        status: TaskStatus = data.get("status", current_task.status)

        updated_task = replace(
            current_task,
            title=title,
            description=data.get("description", current_task.description),
            priority=data.get("priority", current_task.priority),
            status=status,
        )

        return self._repository.update(updated_task)
