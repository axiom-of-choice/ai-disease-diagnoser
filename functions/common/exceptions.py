class AppError(Exception):
    """Excepción base para errores esperados de la app."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class InvalidInputError(AppError):
    """Excepción para errores de entrada inválida."""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
class InvalidOutputError(AppError):
    """Excepción para errores de salida inválida."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)
        
class OpenAIError(AppError):
    """Excepción para errores de OpenAI."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

class FileNotFoundError(AppError):
    """Excepción para errores de archivo no encontrado."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)
        
class DownloadFileError(AppError):
    """Excepción para errores de descarga de archivo."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

class InvalidAudioFormatError(AppError):
    """Excepción para errores de formato de audio inválido."""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
        
class InvalidFileExtensionError(AppError):
    """Excepción para errores de extensión de archivo inválida."""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
        
class TranscriptionError(AppError):
    """Excepción para errores de transcripción."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)
        
class JsonDecodeError(AppError):
    """Excepción para errores de decodificación JSON."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)