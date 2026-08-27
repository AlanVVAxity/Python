from modulo_03.mensajes import construir_mensaje, crear_formateador_mensaje


def test_crear_formateador_mensaje() -> None:
    formatear = crear_formateador_mensaje(
        prefijo="Hola",
        empresa="Empresa Demo",
    )

    mensaje = formatear(
        "Ana",
        "tu solicitud fue recibida.",
    )

    assert mensaje == "Hola Ana, tu solicitud fue recibida. — Empresa Demo"


def test_formateadores_conservan_configuraciones_independientes() -> None:
    formatear_a = crear_formateador_mensaje(
        prefijo="Hola",
        empresa="Empresa A",
    )
    formatear_b = crear_formateador_mensaje(
        prefijo="Buen día",
        empresa="Empresa B",
    )

    assert formatear_a("Ana", "mensaje") == "Hola Ana, mensaje — Empresa A"
    assert formatear_b("Bruno", "mensaje") == ("Buen día Bruno, mensaje — Empresa B")


def test_construir_mensaje_sin_metadatos() -> None:
    mensaje = construir_mensaje(
        "ana@empresa.com",
        "Primera línea.",
        "Segunda línea.",
    )

    assert mensaje == ("Para: ana@empresa.com\n\n" "Primera línea.\n" "Segunda línea.")


def test_construir_mensaje_con_metadatos() -> None:
    mensaje = construir_mensaje(
        "ana@empresa.com",
        "Tu solicitud fue aprobada.",
        prioridad="alta",
        categoria="notificacion",
    )

    assert mensaje == (
        "Para: ana@empresa.com\n\n"
        "Tu solicitud fue aprobada.\n\n"
        "Prioridad: alta\n"
        "Categoria: notificacion"
    )
