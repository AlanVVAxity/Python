import pytest

from modulo_03.lotes import dividir_en_lotes


def test_dividir_en_lotes_con_cantidad_exacta() -> None:
    lotes = list(dividir_en_lotes([1, 2, 3, 4], 2))

    assert lotes == [[1, 2], [3, 4]]


def test_dividir_en_lotes_con_ultimo_lote_incompleto() -> None:
    lotes = list(dividir_en_lotes([1, 2, 3, 4, 5], 2))

    assert lotes == [[1, 2], [3, 4], [5]]


def test_dividir_en_lotes_con_lista_vacia() -> None:
    lotes = list(dividir_en_lotes([], 2))

    assert lotes == []


def test_dividir_en_lotes_rechaza_tamano_invalido() -> None:
    with pytest.raises(ValueError, match="mayor que cero"):
        list(dividir_en_lotes([1, 2, 3], 0))
