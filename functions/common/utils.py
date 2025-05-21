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

def load_prompt(path: str, texto_clinico: str, replace_text: str) -> str:
    """
    Carga el prompt desde un archivo de texto y reemplaza el marcador con el texto clínico.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            prompt_base = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return prompt_base.replace(replace_text, texto_clinico)