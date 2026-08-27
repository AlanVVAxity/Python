from modulo_05.service import InMemoryTaskRepository, TaskService


def main() -> None:
    repository = InMemoryTaskRepository()
    service = TaskService(repository)

    first_task = service.create_task(
        {
            "title": "Configurar herramientas de calidad",
            "priority": "high",
            "description": "Instalar y configurar mypy, ruff, black e isort.",
        }
    )

    updated_task = service.update_task(
        first_task.id,
        {
            "status": "in_progress",
        },
    )

    print("Tareas registradas:")
    for task in service.list_tasks():
        print(
            f"[{task.id}] {task.title} | "
            f"prioridad={task.priority} | estado={task.status}"
        )

    print(f"\nTarea actualizada: {updated_task}")


if __name__ == "__main__":
    main()
