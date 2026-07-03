import { useState, useEffect } from "react";
import type { TemplateInfo } from "../api";
import { fetchTemplates } from "../api";

export default function TemplatesPanel() {
  const [templates, setTemplates] = useState<TemplateInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTemplates()
      .then(setTemplates)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="panel templates-panel">
      <h2>Шаблоны документов</h2>
      {loading && <div className="loading">Загрузка...</div>}
      {!loading && templates.length === 0 && (
        <p className="placeholder">Нет доступных шаблонов. Используйте раздел «Профиль» для настройки применимости.</p>
      )}
      {templates.map((t) => (
        <div key={t.id} className="template-card">
          <h3>{t.title}</h3>
          <p>{t.description}</p>
          <button disabled>Сгенерировать</button>
        </div>
      ))}
      <div className="template-card">
        <h3>Правила внутреннего контроля (ПВК)</h3>
        <p>Шаблон ПВК для кредитной организации на основе 115-ФЗ</p>
        <button disabled>В разработке</button>
      </div>
      <div className="template-card">
        <h3>Анкета клиента</h3>
        <p>Шаблон анкеты для идентификации и оценки риска</p>
        <button disabled>В разработке</button>
      </div>
    </div>
  );
}
