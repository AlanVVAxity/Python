import logging
import subprocess
import sys


def run_python_version_check(logger: logging.Logger) -> str:
    """Ejecuta una verificación externa de la versión de Python."""

    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        message = (
            "Falló la verificación de la versión de Python. "
            f"Código de salida: {error.returncode}"
        )
        logger.exception(message)
        raise RuntimeError(message) from error

    version = result.stdout.strip() or result.stderr.strip()

    if not version:
        message = "No se pudo obtener la versión de Python."
        logger.error(message)
        raise RuntimeError(message)

    logger.info("Verificación de Python completada: %s", version)

    return version
