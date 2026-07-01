__anchor__ = "export"
# schema-ref: project-schema.yaml#/services/14

import json
from datetime import UTC, datetime
from typing import Any

from backend.apps.export.app.schemas.export import ExportRequest, ExportResponse


class ExportService:
    """Generates downloadable reports from structured data.

    Supports JSON format natively. DOCX/PDF/XLSX will be added when the
    corresponding libraries (python-docx, reportlab, openpyxl) are added
    to project dependencies.
    """

    FORMAT_CONFIG: dict[str, dict[str, Any]] = {
        "json": {"content_type": "application/json", "ext": "json"},
        "docx": {
            "content_type": (
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document"
            ),
            "ext": "docx",
        },
        "pdf": {"content_type": "application/pdf", "ext": "pdf"},
        "xlsx": {
            "content_type": (
                "application/vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            ),
            "ext": "xlsx",
        },
    }

    async def export(self, payload: ExportRequest) -> ExportResponse:
        fmt = payload.format
        config = self.FORMAT_CONFIG.get(fmt, self.FORMAT_CONFIG["json"])

        if fmt == "json":
            data = self._build_json(payload)
        elif fmt == "docx":
            data = self._build_stub(payload, "DOCX")
        elif fmt == "pdf":
            data = self._build_stub(payload, "PDF")
        elif fmt == "xlsx":
            data = self._build_stub(payload, "XLSX")
        else:
            data = self._build_json(payload)

        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        safe_title = payload.title.replace(" ", "_").lower()[:40]
        filename = f"{safe_title}_{timestamp}.{config['ext']}"

        return ExportResponse(
            format=fmt,
            filename=filename,
            content_type=config["content_type"],
            data=data,
        )

    def _build_json(self, payload: ExportRequest) -> str:
        doc: dict[str, Any] = {
            "title": payload.title,
            "generated_at": datetime.now(UTC).isoformat(),
            "sections": [],
        }
        for s in payload.sections:
            doc["sections"].append({
                "title": s.title,
                "content": s.content,
                "citations": s.citations,
            })
        if payload.summary:
            doc["summary"] = payload.summary
        return json.dumps(doc, ensure_ascii=False, indent=2)

    def _build_stub(self, payload: ExportRequest, fmt_name: str) -> str:
        lines = [f"=== {fmt_name.upper()} EXPORT STUB ===", f"Title: {payload.title}", ""]
        for s in payload.sections:
            lines.append(f"## {s.title}")
            lines.append(s.content)
            if s.citations:
                lines.append(f"Citations: {', '.join(s.citations)}")
            lines.append("")
        if payload.summary:
            lines.append(f"Summary: {payload.summary}")
        return "\n".join(lines)
