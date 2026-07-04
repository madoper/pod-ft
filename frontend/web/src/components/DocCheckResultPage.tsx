import type { CheckResultData, FindingData } from "../api";

interface Props {
  result: CheckResultData;
  onNewCheck: () => void;
}

function findingIcon(type: string): string {
  switch (type) {
    case "matched_fragment": return "✓";
    case "insufficient_coverage": return "⚠";
    case "no_regulatory_match": return "✗";
    default: return "●";
  }
}

function findingColor(type: string): string {
  switch (type) {
    case "matched_fragment": return "#2e7d32";
    case "insufficient_coverage": return "#e65100";
    case "no_regulatory_match": return "#c62828";
    default: return "#555";
  }
}

function findingBg(type: string): string {
  switch (type) {
    case "matched_fragment": return "#e8f5e9";
    case "insufficient_coverage": return "#fff3e0";
    case "no_regulatory_match": return "#ffebee";
    default: return "#f5f5f5";
  }
}

function confidenceLabel(score: number): string {
  if (score >= 0.8) return "Высокая";
  if (score >= 0.5) return "Средняя";
  return "Низкая";
}

function confidenceColor(score: number): string {
  if (score >= 0.8) return "#2e7d32";
  if (score >= 0.5) return "#e65100";
  return "#c62828";
}

function isGap(f: FindingData): boolean {
  return f.finding_type === "insufficient_coverage" || f.finding_type === "no_regulatory_match";
}

function typeLabel(type: string): string {
  switch (type) {
    case "matched_fragment": return "Соответствие";
    case "insufficient_coverage": return "Недостаточно";
    case "no_regulatory_match": return "Не найдено";
    default: return type;
  }
}

export default function DocCheckResultPage({ result, onNewCheck }: Props) {
  const gapFindings = result.findings.filter(isGap);
  const hasGaps = gapFindings.length > 0;

  return (
    <div className="doc-check-result">
      <div className="result-header">
        <h2>Результат проверки</h2>
        <button onClick={onNewCheck}>Новая проверка</button>
      </div>

      <div className={`coverage-card ${hasGaps ? "insufficient" : "sufficient"}`}>
        <div className="coverage-status">
          <span className="coverage-icon">{hasGaps ? "⚠" : "✓"}</span>
          <div>
            <div className="coverage-title">
              {hasGaps ? "Требуются доработки" : "Достаточное покрытие"}
            </div>
            <div className="coverage-meta">
              Найдено фрагментов: {result.total_fragments_found} · Всего замечаний: {result.findings.length}
            </div>
          </div>
        </div>
        <p className="coverage-summary">{result.coverage_summary}</p>
      </div>

      {hasGaps && (
        <div className="result-section">
          <h3>⚠ Замечания и пробелы</h3>
          {gapFindings.map((f, i) => (
            <div
              key={i}
              className="finding-card gap-finding"
              style={{ borderLeftColor: findingColor(f.finding_type) }}
            >
              <div className="finding-header">
                <span
                  className="finding-type-badge"
                  style={{ background: findingBg(f.finding_type), color: findingColor(f.finding_type) }}
                >
                  {findingIcon(f.finding_type)} {typeLabel(f.finding_type)}
                </span>
                <span
                  className="confidence-badge"
                  style={{ color: confidenceColor(f.confidence) }}
                >
                  {confidenceLabel(f.confidence)}
                </span>
              </div>
              <p className="finding-summary">{f.summary}</p>
            </div>
          ))}
        </div>
      )}

      <div className="result-section">
        <h3>✓ Все находки ({result.findings.length})</h3>
        <div className="findings-table-header">
          <span className="ft-col-type">Тип</span>
          <span className="ft-col-confidence">Достоверность</span>
          <span className="ft-col-citation">Источник</span>
          <span className="ft-col-summary">Описание</span>
        </div>
        {result.findings.map((f, i) => (
          <div key={i} className="finding-row" style={{ borderLeftColor: findingColor(f.finding_type) }}>
            <span className="ft-col-type">
              <span
                className="finding-type-badge"
                style={{ background: findingBg(f.finding_type), color: findingColor(f.finding_type) }}
              >
                {typeLabel(f.finding_type)}
              </span>
            </span>
            <span className="ft-col-confidence">
              <span className="confidence-dot" style={{ background: confidenceColor(f.confidence) }} />
              {confidenceLabel(f.confidence)}
            </span>
            <span className="ft-col-citation">{f.citation_label || "—"}</span>
            <span className="ft-col-summary">
              <span className="finding-summary-text">{f.summary}</span>
              {f.fragment_text && <span className="finding-fragment">{f.fragment_text}</span>}
            </span>
          </div>
        ))}
      </div>

      {result.export_links && result.export_links.length > 0 && (
        <div className="result-section export-section">
          <h3>📥 Экспорт результатов</h3>
          <div className="export-buttons">
            {result.export_links.map((link, i) => (
              <a
                key={i}
                href={link.url}
                className="export-btn"
                target="_blank"
                rel="noopener noreferrer"
              >
                {link.format === "json" && "📄 "}
                {link.format === "docx" && "📝 "}
                {link.format === "pdf" && "📕 "}
                {link.format === "xlsx" && "📊 "}
                {link.label}
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
