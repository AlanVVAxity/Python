from pathlib import Path


def project_root() -> Path:
    """Devuelve la carpeta raíz del proyecto."""

    return Path(__file__).resolve().parents[2]


def data_directory() -> Path:
    """Devuelve la carpeta de archivos de entrada."""

    directory = project_root() / "data"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def output_directory() -> Path:
    """Devuelve y crea, si es necesario, la carpeta de resultados."""

    directory = project_root() / "output"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def logs_directory() -> Path:
    """Devuelve y crea, si es necesario, la carpeta de logs."""

    directory = project_root() / "logs"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def input_csv_path() -> Path:
    """Devuelve la ruta del archivo CSV de ventas."""

    return data_directory() / "ventas.csv"


def output_json_path() -> Path:
    """Devuelve la ruta del archivo JSON generado."""

    return output_directory() / "resumen_ventas.json"


def log_file_path() -> Path:
    """Devuelve la ruta del archivo principal de logs."""

    return logs_directory() / "modulo_06.log"
