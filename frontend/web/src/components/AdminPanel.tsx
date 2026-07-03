import { useState, useEffect } from "react";
import type { BlockedItem } from "../api";
import { fetchAdminBlocks } from "../api";

export default function AdminPanel() {
  const [blocks, setBlocks] = useState<BlockedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchAdminBlocks()
      .then(setBlocks)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="panel admin-panel"><h2>Блокировки</h2><div className="loading">Загрузка...</div></div>;
  if (error) return <div className="panel admin-panel"><h2>Блокировки</h2><div className="error">{error}</div></div>;

  return (
    <div className="panel admin-panel">
      <h2>Блокировки ({blocks.length})</h2>
      {blocks.length === 0 ? (
        <p className="placeholder">Нет активных блокировок</p>
      ) : (
        <ul>
          {blocks.map((b) => (
            <li key={b.id} className="blocked-item">
              <strong>{b.id}</strong>
              <span className="type-badge">{b.type}</span>
              <p>{b.reason}</p>
              <small>Заблокировано: {new Date(b.blocked_at).toLocaleString("ru-RU")}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
