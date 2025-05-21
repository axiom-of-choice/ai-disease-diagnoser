import uuid
import pytest
from functions.common import utils
def test_normalize_text():
    input_text = "  Hello WORLD  "
    expected = "hello world"
    assert utils.normalize_text(input_text) == expected

def test_write_and_read_file(tmp_path):
    # Create a temporary file path
    file_path = tmp_path / "test_file.bin"
    content = b"Sample bytes content"
    
    # Test writing
    utils.write_file(str(file_path), content)
    # Test reading
    read_content = utils.read_file(str(file_path))
    assert read_content == content

def test_generate_uuid():
    uuid_str = utils.generate_uuid()
    # Check valid UUID v4 format
    uuid_obj = uuid.UUID(uuid_str)
    assert isinstance(uuid_obj, uuid.UUID)
    # Version 4 UUID should have version attribute == 4
    assert uuid_obj.version == 4

def test_load_prompt(tmp_path):
    # Prepare a temporary prompt file with a placeholder
    prompt_text = "This is a template: [PLACEHOLDER]. End of prompt."
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text(prompt_text, encoding="utf-8")
    
    # Use load_prompt to replace the placeholder
    replacement = "Clinical text"
    loaded_prompt = utils.load_prompt(str(prompt_file), replacement, "[PLACEHOLDER]")
    
    expected = "This is a template: Clinical text. End of prompt."
    assert loaded_prompt == expected

def test_load_prompt_file_not_found(tmp_path):
    non_existent = tmp_path / "nonexistent.txt"
    with pytest.raises(FileNotFoundError):
        utils.load_prompt(str(non_existent), "text", "[PLACEHOLDER]")

def test_validate_extension_valid(monkeypatch):
    # Simulate a scenario where ValidExtensions returns an enum with .value attributes.
    # We assume one valid extension exists:
    valid_value = ".wav"
    dummy = type("dummyEnum", (), {"value": valid_value})
    monkeypatch.setattr(utils, "ValidExtensions", [dummy])
    
    # valid extension
    assert utils.validate_extension(valid_value)
    # invalid extension
    assert not utils.validate_extension(".mp3")

def test_get_file_extension():
    # Based on the current implementation, the function splits by '/'
    filepath = "/path/to/file/example.txt"
    # Note: This function returns the filename not just extension per docstring.
    # Expected behavior: returns "example.txt"
    result = utils.get_file_extension(filepath)
    assert result == "example.txt"

def test_get_file_extension_error(monkeypatch):
    # Force an exception in get_file_extension by monkeypatching split to raise exception
    def fake_split(_):
        raise Exception("Error")
    
    monkeypatch.setattr(str, "split", fake_split)
    # Verify that returning None on error
    result = utils.get_file_extension("anypath")
    assert result is None