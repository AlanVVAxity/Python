import pytest

from modulo_05.service import InMemoryTaskRepository, TaskService


def test_service_creates_task() -> None:
    service = TaskService(InMemoryTaskRepository())

    task = service.create_task(
        {
            "title": "Configurar mypy",
            "priority": "high",
        }
    )

    assert task.id == 1
    assert task.title == "Configurar mypy"
    assert task.priority == "high"
    assert task.status == "pending"


def test_service_updates_task() -> None:
    service = TaskService(InMemoryTaskRepository())
    task = service.create_task(
        {
            "title": "Crear proyecto",
            "priority": "medium",
        }
    )

    updated_task = service.update_task(
        task.id,
        {
            "status": "completed",
            "priority": "low",
        },
    )

    assert updated_task.status == "completed"
    assert updated_task.priority == "low"


def test_service_rejects_empty_title() -> None:
    service = TaskService(InMemoryTaskRepository())

    with pytest.raises(ValueError, match="título no puede estar vacío"):
        service.create_task(
            {
                "title": "   ",
                "priority": "low",
            }
        )


def test_service_fails_when_task_does_not_exist() -> None:
    service = TaskService(InMemoryTaskRepository())

    with pytest.raises(KeyError, match="no existe"):
        service.update_task(
            99,
            {
                "status": "completed",
            },
        )
