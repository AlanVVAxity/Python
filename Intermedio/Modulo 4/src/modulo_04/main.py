"""Punto de entrada para ejecutar los ejercicios del módulo."""

import asyncio
import cProfile
import pstats
from pathlib import Path
from timeit import timeit

from modulo_04.async_fetcher import fetch_all_async
from modulo_04.config import CPU_NUMBERS, URLS
from modulo_04.cpu_bound import (
    count_primes_parallel,
    count_primes_sequential,
)
from modulo_04.metrics import measure_execution
from modulo_04.sync_fetcher import fetch_all_sync

PROFILE_FILE = Path("cpu_profile.prof")


def run_http_comparison() -> None:
    """Compara la ejecución síncrona con la asíncrona."""
    sync_results, sync_time = measure_execution(fetch_all_sync, URLS)

    async_results, async_time = asyncio.run(_measure_async_execution())

    print("Comparación de solicitudes HTTP")
    print("-" * 40)
    print(f"Solicitudes síncronas completadas: {len(sync_results)}")
    print(f"Tiempo síncrono: {sync_time:.2f} segundos")
    print(f"Solicitudes asíncronas completadas: {len(async_results)}")
    print(f"Tiempo asíncrono: {async_time:.2f} segundos")


async def _measure_async_execution() -> tuple[list[object], float]:
    """Mide una ejecución asíncrona."""
    start_time = asyncio.get_running_loop().time()
    results = await fetch_all_async(URLS)
    elapsed_time = asyncio.get_running_loop().time() - start_time

    return results, elapsed_time


def run_cpu_comparison() -> None:
    """Compara cálculo secuencial y cálculo en procesos separados."""
    sequential_results, sequential_time = measure_execution(
        count_primes_sequential,
        CPU_NUMBERS,
    )
    parallel_results, parallel_time = measure_execution(
        count_primes_parallel,
        CPU_NUMBERS,
    )

    print("\nComparación de cálculos intensivos de CPU")
    print("-" * 40)
    print(f"Resultados secuenciales: {sequential_results}")
    print(f"Tiempo secuencial: {sequential_time:.2f} segundos")
    print(f"Resultados paralelos: {parallel_results}")
    print(f"Tiempo paralelo: {parallel_time:.2f} segundos")


def run_timeit_measurement() -> None:
    """Mide varias ejecuciones secuenciales usando timeit."""
    execution_time = timeit(
        "count_primes_sequential(CPU_NUMBERS)",
        globals={
            "CPU_NUMBERS": CPU_NUMBERS,
            "count_primes_sequential": count_primes_sequential,
        },
        number=3,
    )

    print("\nMedición con timeit")
    print("-" * 40)
    print(f"Tiempo total de 3 ejecuciones secuenciales: {execution_time:.2f} segundos")


def create_cpu_profile() -> None:
    """Genera un archivo de perfilado para el cálculo secuencial."""
    profiler = cProfile.Profile()
    profiler.enable()

    count_primes_sequential(CPU_NUMBERS)

    profiler.disable()
    profiler.dump_stats(PROFILE_FILE)

    print(f"\nPerfil guardado en: {PROFILE_FILE}")

    statistics = pstats.Stats(profiler)
    statistics.sort_stats("cumulative")
    statistics.print_stats(10)


def main() -> None:
    """Ejecuta todas las comparaciones del módulo."""
    run_http_comparison()
    run_cpu_comparison()
    run_timeit_measurement()
    create_cpu_profile()


if __name__ == "__main__":
    main()
