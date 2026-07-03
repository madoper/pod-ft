import { useState, useEffect } from "react";
import { fetchSources, fetchSubscription } from "../api";

export default function DashboardPanel() {
  const [sourceCount, setSourceCount] = useState(0);
  const [quotaUsed, setQuotaUsed] = useState(0);
  const [quotaLimit, setQuotaLimit] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [sources, sub] = await Promise.all([
          fetchSources(),
          fetchSubscription("demo").catch(() => null),
        ]);
        setSourceCount(sources.length);
        if (sub) {
          setQuotaUsed(sub.queries_used);
          setQuotaLimit(sub.queries_limit);
        }
      } catch { /* ignore */ } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) return <div className="panel dashboard-panel"><h2>Панель управления</h2><div className="loading">Загрузка...</div></div>;

  return (
    <div className="panel dashboard-panel">
      <h2>Панель управления</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <span className="stat-value">{sourceCount}</span>
          <span className="stat-label">Активных источников</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{quotaLimit > 0 ? `${quotaUsed}/${quotaLimit}` : "—"}</span>
          <span className="stat-label">Запросов в месяц</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">Tier-1</span>
          <span className="stat-label">Уровень источников</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">✓</span>
          <span className="stat-label">Система готова</span>
        </div>
      </div>
      {quotaLimit > 0 && (
        <div className="info-section">
          <h3>Использование квоты</h3>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${Math.min(100, (quotaUsed / quotaLimit) * 100)}%` }} />
          </div>
        </div>
      )}
    </div>
  );
}
