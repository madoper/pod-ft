__anchor__ = "doc-check"
# schema-ref: project-schema.yaml#/services/12

import uuid
from datetime import UTC, datetime
from typing import Any

from backend.apps.doc_check.app.schemas.check import (
    CheckResponse,
    Finding,
    JobStatusResponse,
)
from backend.apps.retrieval.app.services.retrieval_service import RetrievalService
from backend.apps.verification.app.services.sufficiency_policy import SufficiencyPolicy


class DocCheckService:
    """Verifies an internal document against applicable regulatory fragments.

    In Sprint 5 this will be an async job. For Sprint 4 it runs synchronously
    and uses the same retrieval + verification pipeline as the answer service.
    """

    def __init__(self) -> None:
        self._retrieval = RetrievalService()
        self._policy = SufficiencyPolicy()
        self._jobs: dict[str, dict[str, Any]] = {}

    async def run_check(
        self,
        tenant_id: str,  # noqa: ARG002
        document_text: str,
        document_title: str,  # noqa: ARG002
        document_type: str = "internal_policy",  # noqa: ARG002
        subject_type: str | None = None,
    ) -> CheckResponse:
        job_id = str(uuid.uuid4())
        now = datetime.now(UTC).isoformat()

        # Step 1: search for relevant regulatory fragments
        fragments = await self._retrieval.search(
            query=document_text,
            subject_type=subject_type,
            top_k=20,
        )

        # Step 2: evaluate sufficiency
        decision = self._policy.evaluate_fragments(fragments)

        # Step 3: build findings
        findings: list[Finding] = []
        if not decision.allowed:
            findings.append(Finding(
                finding_type="insufficient_coverage",
                summary=(
                    f"Document does not meet regulatory evidence threshold:"
                    f" {decision.reason_code}"
                ),
                confidence=0.0,
            ))

        for f in fragments[:10]:
            findings.append(Finding(
                finding_type="matched_fragment",
                summary="Relevant regulatory requirement found",
                citation_label=f.get("citation_label"),
                fragment_text=f.get("fragment_text", "")[:200],
                confidence=f.get("confidence", 0),
            ))

        if not findings:
            findings.append(Finding(
                finding_type="no_regulatory_match",
                summary="No applicable regulatory fragments found for this document",
                confidence=0.0,
            ))

        if decision.allowed:
            coverage = (
                f"Found {len(fragments)} relevant Tier-1 fragments."
                f" Document coverage meets sufficiency threshold."
            )
        else:
            coverage = (
                f"Found {len(fragments)} relevant fragments but insufficient:"
                f" {decision.reason_code}. Consider revising document."
            )

        result = CheckResponse(
            job_id=job_id,
            status="completed",
            total_fragments_found=len(fragments),
            findings=findings,
            coverage_summary=coverage,
            created_at=now,
        )

        self._jobs[job_id] = {
            "status": "completed",
            "progress": 100,
            "result": result,
        }
        return result

    async def get_job(self, job_id: str) -> JobStatusResponse | None:
        job = self._jobs.get(job_id)
        if not job:
            return None
        return JobStatusResponse(
            job_id=job_id,
            status=job["status"],
            progress=job.get("progress", 0),
            result=job.get("result"),
            error_message=job.get("error_message"),
        )
