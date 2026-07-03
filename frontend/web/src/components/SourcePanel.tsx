import { useState, useEffect } from "react";
import { fetchSources } from "../api";

export default function SourcePanel() {
  const [sources, setSources] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSources()
      .then(setSources)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="panel source-panel"><h2>Источники</h2><div className="loading">Загрузка...</div></div>;
  if (error) return <div className="panel source-panel"><h2>Источники</h2><div className="error">{error}</div></div>;

  return (
    <div className="panel source-panel">
      <h2>Источники ({sources.length})</h2>
      <ul>
        {sources.map((s, i) => (
          <li key={i}>
            <strong>{s.title || s.name || "?"}</strong>
            {s.version && <span> v{s.version}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}
