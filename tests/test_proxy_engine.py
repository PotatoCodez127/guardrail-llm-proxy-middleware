# tests/test_proxy_engine.py
from unittest.mock import AsyncMock, patch

import pytest

from guardrail_proxy.config import ProxySettings
from guardrail_proxy.engine import GuardrailEngine


@pytest.fixture
def mock_settings():
    return ProxySettings(
        ollama_api_base_url="https://mock.ollama.com",
        ollama_api_key="sk_test_mock_key_abc123",
        primary_model="gemma4:31b-cloud",
        judge_model="gemma4:31b-cloud"
    )

@pytest.mark.asyncio
async def test_evaluate_safety_happy_path(mock_settings):
    engine = GuardrailEngine(settings=mock_settings)
    mock_response = {
        "message": {
            "content": '{"safe": true, "reason": "Response is aligned with travel patterns."}'
        }
    }

    with patch.object(engine.client, 'chat', new_callable=AsyncMock) as mocked_chat:
        mocked_chat.return_value = mock_response
        result = await engine.evaluate_safety("Suggest a museum in Paris", "Visit the Louvre.")

        assert result.safe is True
        assert "aligned" in result.reason
        mocked_chat.assert_called_once()

@pytest.mark.asyncio
async def test_evaluate_safety_malformed_json_fallback(mock_settings):
    engine = GuardrailEngine(settings=mock_settings)
    mock_response = {
        "message": {
            "content": "INVALID RAW STRING WITHOUT JSON STRUCTURE"
        }
    }

    with patch.object(engine.client, 'chat', new_callable=AsyncMock) as mocked_chat:
        mocked_chat.return_value = mock_response
        result = await engine.evaluate_safety("Violate rule", "Malicious output")

        assert result.safe is False
        assert "Syntax validation anomaly" in result.reason
