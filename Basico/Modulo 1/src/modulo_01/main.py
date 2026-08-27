from modulo_01.saludo import crear_saludo


def main() -> None:
    """Ejecuta el programa principal del módulo."""
    mensaje = crear_saludo("Estudiante")
    print(mensaje)


if __name__ == "__main__":
    main()
