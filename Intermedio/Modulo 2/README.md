## Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Consulta el estado de la API. |
| `POST` | `/orders` | Crea una orden. |
| `GET` | `/orders` | Lista las órdenes registradas. |
| `GET` | `/orders/{order_id}` | Obtiene una orden por su identificador. |
| `PUT` | `/orders/{order_id}` | Actualiza una orden existente. |
| `DELETE` | `/orders/{order_id}` | Elimina una orden existente. |

## Documentación interactiva

Con la aplicación ejecutándose, la documentación OpenAPI está disponible en:

```text
http://127.0.0.1:8000/docs