def crear_saludo(nombre: str) -> str:
    """Crea un mensaje de bienvenida para la persona indicada."""
    nombre_limpio = nombre.strip()

    if not nombre_limpio:
        raise ValueError("El nombre no puede estar vacío.")

    return f"Hola, {nombre_limpio}. ¡Tu entorno Python está listo!"
