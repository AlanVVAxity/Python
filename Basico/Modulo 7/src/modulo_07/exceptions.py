class ApiClientError(Exception):
    """Error base para el cliente HTTP."""


class ApiConnectionError(ApiClientError):
    """Error de conexión con el servicio remoto."""


class ApiTimeoutError(ApiClientError):
    """La solicitud excedió el tiempo permitido."""


class ApiResponseError(ApiClientError):
    """El servicio respondió con un error HTTP."""
