from modulo_05.models import Task


def test_task_has_pending_status_by_default() -> None:
    task = Task(
        id=1,
        title="Estudiar tipado",
        priority="medium",
    )

    assert task.status == "pending"
    assert task.description is None
