from collections.abc import Callable


def crear_formateador_mensaje(
    prefijo: str,
    empresa: str,
) -> Callable[[str, str], str]:
    """Crea una función que personaliza mensajes para una empresa."""

    def formatear(nombre: str, contenido: str) -> str:
        return f"{prefijo} {nombre}, {contenido} — {empresa}"

    return formatear


def construir_mensaje(
    destinatario: str,
    *lineas: str,
    **metadatos: str,
) -> str:
    """Construye un mensaje con líneas opcionales y metadatos."""
    cuerpo = "\n".join(lineas)

    if not metadatos:
        return f"Para: {destinatario}\n\n{cuerpo}"

    datos = "\n".join(
        f"{clave.replace('_', ' ').title()}: {valor}"
        for clave, valor in metadatos.items()
    )

    return f"Para: {destinatario}\n\n{cuerpo}\n\n{datos}"
