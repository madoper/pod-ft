import { FileText } from "lucide-react";
import type { CitationLabel } from "../../api";

interface CitationCardProps {
  citation: CitationLabel;
}

export default function CitationCard({ citation }: CitationCardProps) {
  return (
    <div
      style={{
        background: "var(--card-bg)",
        border: "1px solid var(--card-border)",
        borderRadius: "var(--radius-md)",
        padding: "var(--spacing-3)",
        boxShadow: "var(--card-shadow)",
        fontSize: "var(--font-size-sm)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "var(--spacing-2)", marginBottom: "var(--spacing-2)" }}>
        <FileText size={14} style={{ color: "var(--color-primary)", flexShrink: 0 }} />
        <span style={{ fontWeight: 600, color: "var(--color-primary)", fontSize: "var(--font-size-xs)" }}>
          {citation.label || "Источник"}
        </span>
      </div>
      <p style={{ margin: 0, color: "var(--color-text)", lineHeight: "var(--line-height-body)", fontSize: "var(--font-size-xs)" }}>
        {citation.text?.slice(0, 300)}
        {citation.text && citation.text.length > 300 ? "…" : ""}
      </p>
      {citation.source && (
        <span style={{ color: "var(--color-text-secondary)", fontSize: "var(--font-size-xs)", marginTop: "var(--spacing-1)", display: "block" }}>
          {citation.source}
          {citation.version ? ` · ${citation.version}` : ""}
        </span>
      )}
    </div>
  );
}
