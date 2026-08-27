import logging
import subprocess
from unittest.mock import Mock, patch

import pytest

from modulo_06.system_check import run_python_version_check


@patch("modulo_06.system_check.subprocess.run")
def test_returns_python_version(
    mock_run: Mock,
    test_logger: logging.Logger,
) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=["python", "--version"],
        returncode=0,
        stdout="Python 3.12.0\n",
        stderr="",
    )

    version = run_python_version_check(test_logger)

    assert version == "Python 3.12.0"

    mock_run.assert_called_once_with(
        [__import__("sys").executable, "--version"],
        capture_output=True,
        check=True,
        text=True,
    )


@patch("modulo_06.system_check.subprocess.run")
def test_raises_runtime_error_when_check_fails(
    mock_run: Mock,
    test_logger: logging.Logger,
) -> None:
    mock_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=["python", "--version"],
    )

    with pytest.raises(RuntimeError, match="Falló la verificación"):
        run_python_version_check(test_logger)
