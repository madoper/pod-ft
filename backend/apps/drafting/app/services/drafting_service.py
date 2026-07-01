__anchor__ = "drafting"
# schema-ref: project-schema.yaml#/services/13

import uuid
from typing import Any

from backend.apps.drafting.app.schemas.draft import (
    DraftResponse,
    DraftSection,
)
from backend.apps.retrieval.app.services.retrieval_service import RetrievalService


class DraftingService:
    """Generates draft local documents based on applicable regulatory fragments.

    For Sprint 4 this produces a structured outline. In production it will
    use the LLM provider router for full document generation.
    """

    DOCUMENT_TEMPLATES: dict[str, dict[str, Any]] = {
        "pvk": {
            "title": "Правила внутреннего контроля",
            "sections": [
                "Общие положения",
                "Программа идентификации",
                "Порядок фиксирования информации",
                "Порядок информирования Росфинмониторинга",
                "Квалификация и обучение сотрудников",
                "Ответственность",
            ],
        },
        "order": {
            "title": "Приказ о назначении ответственного сотрудника",
            "sections": [
                "Назначение",
                "Обязанности",
                "Ответственность",
            ],
        },
        "checklist": {
            "title": "Чек-лист проверки соблюдения требований",
            "sections": [
                "Идентификация клиентов",
                "Фиксирование информации",
                "Порядок направления сообщений",
                "Внутренний контроль",
            ],
        },
    }

    def __init__(self) -> None:
        self._retrieval = RetrievalService()
        self._drafts: dict[str, dict[str, Any]] = {}

    async def generate_draft(
        self,
        document_type: str,
        subject_type: str | None = None,  # noqa: ARG002
        context: str | None = None,
    ) -> DraftResponse:
        draft_id = str(uuid.uuid4())
        template = self.DOCUMENT_TEMPLATES.get(document_type)
        if not template:
            template = {
                "title": f"Документ типа {document_type}",
                "sections": ["Общие положения"],
            }

        query = context or template["title"]
        fragments = await self._retrieval.search(query=query, top_k=10)

        sections = []
        for sec_title in template["sections"]:
            sec_fragments = [
                f for f in fragments
                if any(
                    w in (f.get("fragment_text") or "").lower()
                    for w in sec_title.lower().split()[:3]
                )
            ][:3]
            citations = [
                f.get("citation_label", "")
                for f in sec_fragments
                if f.get("citation_label")
            ]
            sample_text = (
                sec_fragments[0].get("fragment_text", "")[:150]
                if sec_fragments
                else "Раздел требует разработки в соответствии с типовой структурой."
            )
            sections.append(DraftSection(
                title=sec_title,
                content=(
                    f"На основе требований:\n{sample_text}"
                    if sec_fragments else "Требуется разработка"
                ),
                citations=citations,
            ))

        # Summary
        matched = sum(1 for s in sections if s.citations)
        summary = (
            f"Сгенерирован проект '{template['title']}'. "
            f"Найдено нормативных ссылок: {len(fragments)}. "
            f"Разделов с обоснованием: {matched}/{len(sections)}."
        )

        result = DraftResponse(
            draft_id=draft_id,
            document_type=document_type,
            title=template["title"],
            sections=sections,
            summary=summary,
        )

        self._drafts[draft_id] = result.model_dump()
        return result
