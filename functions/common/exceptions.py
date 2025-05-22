class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class InvalidInputError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
class InvalidOutputError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)
        
class OpenAIError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

class FileNotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)
        
class DownloadFileError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)

class InvalidAudioFormatError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
        
class InvalidFileExtensionError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)
        
class TranscriptionError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)
        
class JsonDecodeError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=500)