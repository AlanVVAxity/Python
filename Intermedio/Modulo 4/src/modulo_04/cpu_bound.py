"""Funciones para ejecutar cálculos intensivos de CPU."""

from concurrent.futures import ProcessPoolExecutor


def count_primes(limit: int) -> int:
    """Cuenta los números primos menores o iguales que limit."""
    total = 0

    for number in range(2, limit + 1):
        is_prime = True

        for divisor in range(2, int(number**0.5) + 1):
            if number % divisor == 0:
                is_prime = False
                break

        if is_prime:
            total += 1

    return total


def count_primes_sequential(limits: list[int]) -> list[int]:
    """Ejecuta los cálculos de CPU en secuencia."""
    return [count_primes(limit) for limit in limits]


def count_primes_parallel(limits: list[int]) -> list[int]:
    """Ejecuta los cálculos de CPU en procesos separados."""
    with ProcessPoolExecutor() as executor:
        return list(executor.map(count_primes, limits))
