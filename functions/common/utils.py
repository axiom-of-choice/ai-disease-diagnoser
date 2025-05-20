import uuid

def normalize_text(text: str) -> str:
    return text.strip().lower()

def write_file(file_path: str, content: bytes) -> None:
    with open(file_path, "wb") as file:
        try:
            file.write(content)
        except Exception as e:
            raise IOError(f"Error writing to file {file_path}: {e}")

def read_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        try:
            return file.read()
        except Exception as e:
            raise IOError(f"Error reading file {file_path}: {e}")
        
def generate_uuid() -> str:
    return str(uuid.uuid4())