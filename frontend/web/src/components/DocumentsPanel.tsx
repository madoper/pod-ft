import { useState, useEffect } from "react";
import type { SourceItem } from "../api";
import { fetchSourcesDetail } from "../api";

export default function DocumentsPanel() {
  const [sources, setSources] = useState<SourceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSourcesDetail()
      .then(setSources)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="panel documents-panel"><h2>Каталог документов</h2><div className="loading">Загрузка...</div></div>;
  if (error) return <div className="panel documents-panel"><h2>Каталог документов</h2><div className="error">{error}</div></div>;

  return (
    <div className="panel documents-panel">
      <h2>Каталог документов</h2>
      <p className="subtitle">Tier-1 официальные источники</p>
      {sources.length === 0 ? (
        <p className="placeholder">Нет зарегистрированных источников</p>
      ) : (
        <table className="sources-table">
          <thead>
            <tr>
              <th>Домен</th>
              <th>Регулятор</th>
              <th>Тип</th>
              <th>Tier</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            {sources.map((s) => (
              <tr key={s.id}>
                <td>{s.domain}</td>
                <td>{s.regulator_name}</td>
                <td>{s.source_type}</td>
                <td><span className="tier-badge">{s.tier}</span></td>
                <td>{s.is_active ? "Активен" : "Неактивен"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
