import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

@patch("medical_ai_common.openai_client.extract_medical_info")
def test_extract_endpoint_success(mock_extract):
    pass
