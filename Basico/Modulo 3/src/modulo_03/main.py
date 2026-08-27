import logging

from modulo_03.lotes import dividir_en_lotes
from modulo_03.mensajes import construir_mensaje, crear_formateador_mensaje
from modulo_03.reintentos import reintentar
from modulo_03.temporizador import Temporizador


def configurar_logging() -> None:
    """Configura los mensajes de registro del proyecto."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )


def main() -> None:
    """Simula el envío de notificaciones en lotes."""
    configurar_logging()

    destinatarios = [
        "ana@empresa.com",
        "bruno@empresa.com",
        "carla@empresa.com",
        "diego@empresa.com",
        "elena@empresa.com",
    ]

    formatear_mensaje = crear_formateador_mensaje(
        prefijo="Hola",
        empresa="Empresa Demo",
    )

    intentos_envio = 0

    @reintentar(
        intentos=3,
        espera_inicial=0.2,
        factor_backoff=2.0,
        excepciones=(ConnectionError,),
    )
    def enviar_lote(destinatarios_lote: list[str]) -> str:
        """Simula un envío que falla temporalmente en el primer intento."""
        nonlocal intentos_envio
        intentos_envio += 1

        if intentos_envio == 1:
            raise ConnectionError("El servicio de notificaciones no responde.")

        return f"Lote enviado a {len(destinatarios_lote)} destinatario(s)."

    with Temporizador("envío de notificaciones") as temporizador:
        for numero_lote, destinatarios_lote in enumerate(
            dividir_en_lotes(destinatarios, 2),
            start=1,
        ):
            mensaje = construir_mensaje(
                destinatarios_lote[0],
                formatear_mensaje(
                    "colaborador",
                    "tienes una notificación pendiente.",
                ),
                prioridad="normal",
                lote=str(numero_lote),
            )

            print(f"\n--- Lote {numero_lote} ---")
            print(mensaje)
            print(enviar_lote(destinatarios_lote))

    print(f"\nTiempo total: {temporizador.duracion:.6f} segundos")


if __name__ == "__main__":
    main()
