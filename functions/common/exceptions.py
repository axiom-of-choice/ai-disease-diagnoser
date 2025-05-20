class AppError(Exception):
    """Excepción base para errores esperados de la app."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)
