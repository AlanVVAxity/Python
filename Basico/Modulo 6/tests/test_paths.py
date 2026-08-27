from pathlib import Path

from modulo_06.paths import (
    data_directory,
    input_csv_path,
    log_file_path,
    logs_directory,
    output_directory,
    output_json_path,
    project_root,
)


def test_project_root_returns_a_path() -> None:
    assert isinstance(project_root(), Path)


def test_data_directory_exists() -> None:
    directory = data_directory()

    assert directory.exists()
    assert directory.name == "data"


def test_output_directory_exists() -> None:
    directory = output_directory()

    assert directory.exists()
    assert directory.name == "output"


def test_logs_directory_exists() -> None:
    directory = logs_directory()

    assert directory.exists()
    assert directory.name == "logs"


def test_expected_file_names() -> None:
    assert input_csv_path().name == "ventas.csv"
    assert output_json_path().name == "resumen_ventas.json"
    assert log_file_path().name == "modulo_06.log"
