__anchor__ = "tests"

import pytest

from backend.apps.verification.app.services.llm_verifier import LlmVerifier
from backend.shared.settings import settings


@pytest.mark.asyncio
async def test_llm_verifier_not_configured() -> None:
    old_key = settings.llm_api_key
    settings.llm_api_key = ""
    try:
        verifier = LlmVerifier()
        result = await verifier.verify(
            question="Test?",
            fragments=[{"fragment_text": "Answer.", "citation_label": "ст. 1", "tier": 1}],
            draft_summary="Test summary",
        )
        assert result["passed"] is True
        assert result["reason"] == "llm_not_configured"
    finally:
        settings.llm_api_key = old_key


@pytest.mark.asyncio
async def test_llm_verifier_build_prompt() -> None:
    verifier = LlmVerifier()
    prompt = verifier._build_prompt(
        question="Какие требования?",
        fragments=[
            {"fragment_text": "Текст фрагмента", "citation_label": "ст. 7", "tier": 1},
        ],
        draft_summary="Проект ответа",
    )
    assert "Какие требования?" in prompt
    assert "ст. 7" in prompt
    assert "Текст фрагмента" in prompt
    assert "Проект ответа" in prompt
    assert "ПОД/ФТ/ФРОМУ" in prompt


def test_llm_verifier_parse_response() -> None:
    result = LlmVerifier._parse_response('{"passed": true, "confidence": 0.95, "reason": "ok"}')
    assert result["passed"] is True
    assert result["confidence"] == 0.95


def test_llm_verifier_parse_response_broken_json() -> None:
    result = LlmVerifier._parse_response("Not JSON at all")
    assert result["passed"] is True
    assert result["reason"] == "parse_fallback"
