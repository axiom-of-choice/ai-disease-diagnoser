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

def load_prompt(path, texto_clinico, replace_text: str):
    """
    Carga el prompt desde un archivo de texto y reemplaza el marcador con el texto clínico.
    """
    with open(path, "r", encoding="utf-8") as file:
        prompt_base = file.read()
    return prompt_base.replace(f"{replace_text}", texto_clinico)