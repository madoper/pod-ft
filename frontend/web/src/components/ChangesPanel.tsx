import { useState } from "react";
import type { ChangeItem } from "../api";
import { fetchChanges } from "../api";

export default function ChangesPanel() {
  const [fromDate, setFromDate] = useState("");
  const [changes, setChanges] = useState<ChangeItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  async function handleSearch() {
    setLoading(true);
    setError("");
    setSearched(true);
    try {
      const items = await fetchChanges(fromDate || undefined);
      setChanges(items);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel changes-panel">
      <h2>Изменения</h2>
      <div className="filter-row">
        <input
          type="date"
          value={fromDate}
          onChange={(e) => setFromDate(e.target.value)}
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? "Поиск..." : "Найти изменения"}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      {searched && !loading && changes.length === 0 && (
        <p className="placeholder">Изменений не найдено</p>
      )}
      {changes.length > 0 && (
        <ul>
          {changes.map((c) => (
            <li key={c.document_id} className="change-item">
              <strong>{c.title}</strong>
              <span className={`change-type change-${c.change_type}`}>{c.change_type}</span>
              {c.summary && <p>{c.summary}</p>}
              {c.version_label && <small>Версия: {c.version_label}{c.effective_from ? ` (с ${c.effective_from})` : ""}</small>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
