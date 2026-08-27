"""Pruebas para los cálculos intensivos de CPU."""

from modulo_04.cpu_bound import (
    count_primes,
    count_primes_parallel,
    count_primes_sequential,
)


def test_count_primes_returns_expected_value() -> None:
    """Verifica el conteo de primos hasta 10."""
    assert count_primes(10) == 4


def test_sequential_and_parallel_results_are_equal() -> None:
    """Verifica que ambas estrategias devuelvan el mismo resultado."""
    limits = [10, 20, 30]

    sequential_results = count_primes_sequential(limits)
    parallel_results = count_primes_parallel(limits)

    assert sequential_results == parallel_results
