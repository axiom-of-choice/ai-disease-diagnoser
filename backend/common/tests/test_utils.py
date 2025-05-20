from common.utils import normalize_text

def test_normalize_text():
    assert normalize_text("  HOLA Mundo  ") == "hola mundo"
