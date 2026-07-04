__anchor__ = "tests"

import pytest

from backend.shared.llm.contracts import LlmRequest
from backend.shared.llm.provider_router import MockProvider, create_llm_router
from backend.shared.settings import settings


@pytest.mark.asyncio
async def test_mock_provider_drafting() -> None:
    provider = MockProvider()
    request = LlmRequest(task_type="drafting", prompt="Test drafting prompt")
    response = await provider.invoke(request)
    assert response.model_used == "mock"
    assert "summary" in response.content


@pytest.mark.asyncio
async def test_mock_provider_verification() -> None:
    provider = MockProvider()
    request = LlmRequest(task_type="verification", prompt="Test verification prompt")
    response = await provider.invoke(request)
    assert response.model_used == "mock"
    assert "is_supported" in response.content


@pytest.mark.asyncio
async def test_mock_provider_extraction() -> None:
    provider = MockProvider()
    request = LlmRequest(task_type="extraction", prompt="Test extraction prompt")
    response = await provider.invoke(request)
    assert response.model_used == "mock"
    assert "norms" in response.content


@pytest.mark.asyncio
async def test_mock_provider_unknown() -> None:
    provider = MockProvider()
    request = LlmRequest(task_type="unknown", prompt="test")
    response = await provider.invoke(request)
    assert response.content == "{}"


@pytest.mark.asyncio
async def test_create_llm_router_no_api_key() -> None:
    old_key = settings.llm_api_key
    settings.llm_api_key = ""
    try:
        router = create_llm_router()
        request = LlmRequest(task_type="drafting", prompt="Test")
        response = await router.invoke(request)
        assert response.model_used == "mock"
    finally:
        settings.llm_api_key = old_key
