import { useState, useRef, type FormEvent } from "react";
import { submitCheck } from "../api";

const API_BASE = "/api/v1";

export default function DocCheckPanel() {
  const [docText, setDocText] = useState("");
  const [docTitle, setDocTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!docText.trim() || !docTitle.trim() || loading) return;

    setLoading(true);
    setProgress(0);
    setResult(null);
    setError("");

    try {
      const { job_id } = await submitCheck(docText, docTitle, "pvk");
      await streamStatus(job_id);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function streamStatus(jobId: string) {
    abortRef.current = new AbortController();

    try {
      const response = await fetch(`${API_BASE}/check/${jobId}/stream`, {
        signal: abortRef.current.signal,
      });
      if (!response.ok || !response.body) {
        throw new Error("SSE connection failed");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(6));

            if (data.status === "not_found" || data.status === "timeout") {
              setError(data.status === "not_found" ? "Задача не найдена" : "Таймаут ожидания");
              return;
            }

            if (data.progress !== undefined) {
              setProgress(data.progress);
            }

            if (data.status === "completed" && data.result) {
              const r = data.result;
              setResult(
                `Найдено фрагментов: ${r.total_fragments_found}\n` +
                  (r.coverage_summary ? `\n${r.coverage_summary}\n` : "") +
                  (r.findings?.length
                    ? "\nРезультаты:\n" +
                      r.findings
                        .map(
                          (f: any, i: number) =>
                            `${i + 1}. [${f.finding_type}] ${(f.summary || "").slice(0, 150)}`,
                        )
                        .join("\n")
                    : "") +
                  (r.export_links?.length
                    ? "\n\nЭкспорт:\n" +
                      r.export_links
                        .map((e: any) => `  ${e.format.toUpperCase()}: ${e.url}`)
                        .join("\n")
                    : ""),
              );
              return;
            }

            if (data.status === "failed") {
              setError(data.error_message || "Проверка не удалась");
              return;
            }
          }
        }
      }
    } catch (err: any) {
      if (err.name !== "AbortError") {
        throw err;
      }
    }
  }

  function handleCancel() {
    abortRef.current?.abort();
    setLoading(false);
  }

  return (
    <div className="panel doc-check-panel">
      <h2>Проверка документа</h2>
      <form onSubmit={handleSubmit}>
        <input
          value={docTitle}
          onChange={(e) => setDocTitle(e.target.value)}
          placeholder="Название документа"
          disabled={loading}
        />
        <textarea
          value={docText}
          onChange={(e) => setDocText(e.target.value)}
          placeholder="Текст документа для проверки..."
          rows={6}
          disabled={loading}
        />
        <div className="filter-row">
          <button type="submit" disabled={loading || !docText.trim() || !docTitle.trim()}>
            {loading ? "Проверка..." : "Проверить"}
          </button>
          {loading && (
            <button type="button" onClick={handleCancel} className="btn-cancel">
              Отмена
            </button>
          )}
        </div>
      </form>
      {loading && (
        <div className="loading">
          Проверяю документ... {progress > 0 && `${progress}%`}
          {progress > 0 && (
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }} />
            </div>
          )}
        </div>
      )}
      {error && <div className="error">{error}</div>}
      {result && <pre className="result">{result}</pre>}
    </div>
  );
}
