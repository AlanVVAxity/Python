from pathlib import Path

from modulo_07.downloader import download_file


def test_download_file_saves_content(
    httpx_mock: object,
    tmp_path: Path,
) -> None:
    content = b"Contenido descargado correctamente."

    httpx_mock.add_response(
        url="https://files.example.com/sample.txt",
        content=content,
        status_code=200,
    )

    destination = tmp_path / "sample.txt"

    result = download_file(
        url="https://files.example.com/sample.txt",
        destination=destination,
    )

    assert result == destination
    assert destination.exists()
    assert destination.read_bytes() == content
