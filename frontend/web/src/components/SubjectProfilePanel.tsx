import { useState } from "react";
import type { SubjectProfileDto } from "../api";
import { createProfile, deleteProfile, fetchProfiles } from "../api";

export default function SubjectProfilePanel() {
  const [tenantId, setTenantId] = useState("demo");
  const [profiles, setProfiles] = useState<SubjectProfileDto[]>([]);
  const [subjectType, setSubjectType] = useState("credit_organization");
  const [regulator, setRegulator] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLoad() {
    setLoading(true);
    setError("");
    try {
      const items = await fetchProfiles(tenantId);
      setProfiles(items);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate() {
    setLoading(true);
    setError("");
    try {
      const result = await createProfile(tenantId, subjectType, regulator || undefined);
      if (result) {
        await handleLoad();
        setSubjectType("credit_organization");
        setRegulator("");
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id: string) {
    await deleteProfile(id);
    await handleLoad();
  }

  return (
    <div className="panel subject-profile-panel">
      <h2>Профиль применимости</h2>
      <div className="filter-row">
        <input value={tenantId} onChange={(e) => setTenantId(e.target.value)} placeholder="Tenant ID" />
        <button onClick={handleLoad} disabled={loading || !tenantId.trim()}>
          {loading ? "Загрузка..." : "Загрузить"}
        </button>
      </div>
      {error && <div className="error">{error}</div>}

      <div className="info-section">
        <h3>Новый профиль</h3>
        <select value={subjectType} onChange={(e) => setSubjectType(e.target.value)}>
          <option value="credit_organization">Кредитная организация</option>
          <option value="article_7_1">Субъект статьи 7.1</option>
          <option value="nfo">Нефинансовая организация</option>
          <option value="professional">Профессиональный участник</option>
        </select>
        <input value={regulator} onChange={(e) => setRegulator(e.target.value)} placeholder="Регулятор (опционально)" />
        <button onClick={handleCreate} disabled={loading}>Создать</button>
      </div>

      {profiles.length > 0 && (
        <ul>
          {profiles.map((p) => (
            <li key={p.id} className="profile-item">
              <strong>{p.subject_type}</strong>
              {p.regulator && <span className="type-badge">{p.regulator}</span>}
              <button className="btn-small btn-danger" onClick={() => handleDelete(p.id!)}>
                Удалить
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
