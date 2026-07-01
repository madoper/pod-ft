__anchor__ = "answer-service"
# schema-ref: project-schema.yaml#/services/10
# schema-ref: production-tech-project-podft-rag-dev-spec.md#/13.2 Answering orchestration

import uuid
from datetime import UTC, date, datetime
from typing import Any

from backend.apps.retrieval.app.services.retrieval_service import RetrievalService
from backend.apps.verification.app.services.sufficiency_policy import SufficiencyPolicy


class AnsweringService:
    """Orchestrates the full answer flow: retrieval → verification → compose.

    Implements the orchestration loop from spec section 13.2.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._retrieval = RetrievalService()
        self._policy = SufficiencyPolicy()

    async def answer(
        self,
        question: str,
        channel: str = "web",
        subject_type: str | None = None,
        regulator: str | None = None,
        as_of_date: date | None = None,  # noqa: ARG002
    ) -> dict[str, Any]:
        session_id = str(uuid.uuid4())
        now = datetime.now(UTC).isoformat()

        session: dict[str, Any] = {
            "session_id": session_id,
            "question": question,
            "channel": channel,
            "status": "pending",
            "created_at": now,
        }
        self._sessions[session_id] = session

        # Step 1: Retrieval — search for relevant fragments
        fragments = await self._retrieval.search(
            query=question,
            subject_type=subject_type,
            regulator=regulator,
            top_k=10,
        )

        # Step 2: Pre-check — sufficiency gate
        decision = self._policy.evaluate_fragments(fragments)
        if not decision.allowed:
            session["status"] = "refused"
            session["reason_code"] = decision.reason_code
            return {
                "session_id": session_id,
                "status": "refused",
                "reason_code": decision.reason_code,
                "evidence_count": len(fragments),
                "answer": None,
            }

        # Step 3: Compose extractive answer
        draft = self._compose_answer(question, fragments)

        # Step 4: Final verification
        draft_decision = self._policy.evaluate_draft(
            draft_summary=draft["summary"],
            citations=[c["citation_label"] for c in draft["citations"]],
        )
        if not draft_decision.allowed:
            session["status"] = "refused"
            session["reason_code"] = draft_decision.reason_code
            return {
                "session_id": session_id,
                "status": "refused",
                "reason_code": draft_decision.reason_code,
                "evidence_count": len(fragments),
                "answer": None,
            }

        # Step 5: Store evidence trail
        evidence = self._build_evidence(fragments)
        session["status"] = "ok"
        session["evidence"] = evidence

        return {
            "session_id": session_id,
            "status": "ok",
            "answer": draft,
            "evidence_count": len(fragments),
            "verifier_status": "approved",
        }

    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        return self._sessions.get(session_id)

    def _compose_answer(
        self, question: str, fragments: list[dict[str, Any]]  # noqa: ARG002
    ) -> dict[str, Any]:
        citations = []
        text_parts = []

        for f in fragments[:5]:
            citation = {
                "fragment_id": f["fragment_id"],
                "document_title": f.get("document_title"),
                "citation_label": f.get("citation_label", ""),
                "quote": f.get("fragment_text", "")[:200],
                "source_url": f.get("source_domain"),
            }
            citations.append(citation)
            text_parts.append(f.get("fragment_text", ""))

        summary = "Based on the retrieved regulatory fragments:\n"
        summary += "\n".join(f"- {p[:100]}" for p in text_parts)

        return {
            "summary": summary,
            "citations": citations,
            "applicability_explanation": [
                f"Query matched {len(fragments)} Tier-1 fragments.",
                f"Candidate fragments meet sufficiency policy: {len(fragments) >= 2}.",
            ],
        }

    def _build_evidence(self, fragments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "fragment_id": f["fragment_id"],
                "score": f.get("score", 0),
                "confidence": f.get("confidence", 0),
                "source": f.get("source_domain"),
            }
            for f in fragments
        ]
