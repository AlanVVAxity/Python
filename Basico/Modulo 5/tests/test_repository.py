from modulo_05.models import Task
from modulo_05.service import InMemoryTaskRepository


def test_repository_adds_and_gets_task() -> None:
    repository = InMemoryTaskRepository()
    task = Task(
        id=repository.get_next_id(),
        title="Crear pruebas",
        priority="high",
    )

    repository.add(task)

    assert repository.get_by_id(task.id) == task


def test_repository_returns_none_for_unknown_task() -> None:
    repository = InMemoryTaskRepository()

    assert repository.get_by_id(999) is None
