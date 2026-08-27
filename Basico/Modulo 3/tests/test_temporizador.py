import pytest

from modulo_03.temporizador import Temporizador


def test_temporizador_mide_duracion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tiempos = iter([10.0, 12.5])

    monkeypatch.setattr(
        "modulo_03.temporizador.perf_counter",
        lambda: next(tiempos),
    )

    with Temporizador("prueba") as temporizador:
        pass

    assert temporizador.nombre == "prueba"
    assert temporizador.duracion == 2.5


def test_temporizador_no_oculta_excepciones() -> None:
    with pytest.raises(ValueError, match="error de prueba"):
        with Temporizador("operación con error"):
            raise ValueError("error de prueba")
