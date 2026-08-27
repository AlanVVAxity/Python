import pytest

from modulo_03.reintentos import reintentar


def test_reintentar_devuelve_resultado_en_primer_intento(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    esperas: list[float] = []

    monkeypatch.setattr(
        "modulo_03.reintentos.sleep",
        lambda segundos: esperas.append(segundos),
    )

    @reintentar(intentos=3)
    def operacion() -> str:
        return "completada"

    assert operacion() == "completada"
    assert esperas == []


def test_reintentar_reintenta_hasta_que_funcion_tiene_exito(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    esperas: list[float] = []
    intentos_realizados = 0

    monkeypatch.setattr(
        "modulo_03.reintentos.sleep",
        lambda segundos: esperas.append(segundos),
    )

    @reintentar(intentos=3, espera_inicial=1.0, factor_backoff=2.0)
    def operacion() -> str:
        nonlocal intentos_realizados
        intentos_realizados += 1

        if intentos_realizados < 3:
            raise ConnectionError("Servicio no disponible.")

        return "completada"

    assert operacion() == "completada"
    assert intentos_realizados == 3
    assert esperas == [1.0, 2.0]


def test_reintentar_lanza_ultima_excepcion_al_agotar_intentos(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "modulo_03.reintentos.sleep",
        lambda segundos: None,
    )

    @reintentar(intentos=2, espera_inicial=0.0)
    def operacion() -> None:
        raise ConnectionError("Servicio no disponible.")

    with pytest.raises(ConnectionError, match="Servicio no disponible"):
        operacion()


def test_reintentar_no_intercepta_excepciones_no_configuradas() -> None:
    @reintentar(excepciones=(ConnectionError,))
    def operacion() -> None:
        raise ValueError("Dato inválido.")

    with pytest.raises(ValueError, match="Dato inválido"):
        operacion()


@pytest.mark.parametrize(
    ("argumentos", "mensaje"),
    [
        ({"intentos": 0}, "al menos 1"),
        ({"espera_inicial": -1.0}, "no puede ser negativa"),
        ({"factor_backoff": 0.5}, "mayor o igual a 1"),
    ],
)
def test_reintentar_valida_su_configuracion(
    argumentos: dict[str, float | int],
    mensaje: str,
) -> None:
    with pytest.raises(ValueError, match=mensaje):
        reintentar(**argumentos)
