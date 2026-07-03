__anchor__ = "tests"

from backend.shared.llm.prompts.drafting import build_drafting_prompt
from backend.shared.llm.prompts.extraction import build_extraction_prompt
from backend.shared.llm.prompts.verification import build_verification_prompt


def test_build_drafting_prompt() -> None:
    evidence = [
        {"citation_label": "п. 1", "fragment_text": "Требование к ПВК", "source": "test"},
    ]
    prompt = build_drafting_prompt("Вопрос?", evidence)
    assert "{question}" not in prompt
    assert "Вопрос?" in prompt
    assert "п. 1" in prompt
    assert "Требование к ПВК" in prompt


def test_build_verification_prompt() -> None:
    evidence = [
        {"citation_label": "п. 3", "fragment_text": "Обязанность", "source": "test"},
    ]
    prompt = build_verification_prompt("Вопрос?", "Черновик ответа", evidence)
    assert "{question}" not in prompt
    assert "Вопрос?" in prompt
    assert "Черновик ответа" in prompt
    assert "п. 3" in prompt


def test_build_extraction_prompt() -> None:
    prompt = build_extraction_prompt("https://example.com/doc", "Текст документа...")
    assert "{source_url}" not in prompt
    assert "https://example.com/doc" in prompt
    assert "Текст документа..." in prompt
