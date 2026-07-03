import { useState, type FormEvent } from "react";
import { submitCheck, pollCheckResult } from "../api";

export default function DocCheckPanel() {
  const [docText, setDocText] = useState("");
  const [docTitle, setDocTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState("");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!docText.trim() || !docTitle.trim() || loading) return;

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const { job_id } = await submitCheck(docText, docTitle, "pvk");
      for (let i = 0; i < 30; i++) {
        const poll = await pollCheckResult(job_id);
        if (poll.status === "completed") {
          const fragments = poll.result?.fragments || [];
          setResult(
            `Найдено фрагментов: ${poll.result?.total_fragments_found || 0}\n` +
              fragments
                .map(
                  (f, j) =>
                    `${j + 1}. [${f.status}] ${f.label}: ${f.text.slice(0, 100)}...`,
                )
                .join("\n"),
          );
          return;
        }
        if (poll.status === "failed") {
          setError(poll.error_message || "Проверка не удалась");
          return;
        }
        await new Promise((r) => setTimeout(r, 1000));
      }
      setError("Таймаут ожидания результата");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
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
        <button type="submit" disabled={loading || !docText.trim() || !docTitle.trim()}>
          {loading ? "Проверка..." : "Проверить"}
        </button>
      </form>
      {loading && <div className="loading">Проверяю документ...</div>}
      {error && <div className="error">{error}</div>}
      {result && (
        <pre className="result">{result}</pre>
      )}
    </div>
  );
}
