import { useState } from "react";
import type { SubscriptionInfo } from "../api";
import { fetchSubscription, fetchQuota } from "../api";

export default function ProfilePanel() {
  const [userId, setUserId] = useState("");
  const [subscription, setSubscription] = useState<SubscriptionInfo | null>(null);
  const [quota, setQuota] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLoad() {
    if (!userId.trim()) return;
    setLoading(true);
    setError("");
    try {
      const [sub, q] = await Promise.all([
        fetchSubscription(userId),
        fetchQuota(userId),
      ]);
      setSubscription(sub);
      setQuota(q);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel profile-panel">
      <h2>Профиль</h2>
      <div className="user-id-input">
        <input
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="ID пользователя"
        />
        <button onClick={handleLoad} disabled={loading || !userId.trim()}>
          {loading ? "Загрузка..." : "Загрузить"}
        </button>
      </div>
      {error && <div className="error">{error}</div>}
      {subscription && (
        <div className="info-section">
          <h3>Подписка</h3>
          <p>План: <strong>{subscription.plan}</strong></p>
          <p>Запросов: {subscription.queries_used} / {subscription.queries_limit}</p>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{
                width: `${Math.min(100, (subscription.queries_used / subscription.queries_limit) * 100)}%`,
              }}
            />
          </div>
          <small>Действует до: {new Date(subscription.expires_at).toLocaleDateString("ru-RU")}</small>
        </div>
      )}
      {quota && (
        <div className="info-section">
          <h3>Квота</h3>
          <p>Доступно: {quota.remaining ?? quota.quota?.remaining ?? "—"}</p>
        </div>
      )}
    </div>
  );
}
