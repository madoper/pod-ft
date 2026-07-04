interface Props {
  onTryDemo: (question: string) => void;
  onNavigate: (tab: string) => void;
}

const DEMO_QUESTION =
  "Какие требования к правилам внутреннего контроля (ПВК) по ПОД/ФТ для кредитной организации?";

const FEATURES = [
  {
    id: "ask",
    title: "Запрос",
    icon: "💬",
    desc: "Задайте вопрос по ПОД/ФТ/ФРОМУ — ИИ найдёт ответ в официальных регуляторных источниках Tier-1 с цитированием конкретных параграфов.",
  },
  {
    id: "check",
    title: "Проверка",
    icon: "📋",
    desc: "Проверьте внутренние документы на соответствие регуляторным требованиям. Система укажет пробелы и недостающие нормы.",
  },
  {
    id: "sources",
    title: "Источники",
    icon: "📚",
    desc: "Каталог активных регуляторных источников Tier-1: Росфинмониторинг, Банк России, официальное опубликование.",
  },
  {
    id: "documents",
    title: "Каталог",
    icon: "📄",
    desc: "База загруженных и обработанных документов с версионированием и статусом.",
  },
  {
    id: "changes",
    title: "Изменения",
    icon: "🔄",
    desc: "Мониторинг изменений в регуляторной базе: новые документы, обновления обязательств, отслеживание версий.",
  },
  {
    id: "subject-profile",
    title: "Профиль",
    icon: "👤",
    desc: "Настройка типа субъекта (кредитная организация, НФО, иное) и выбор регулятора для персонализации ответов.",
  },
  {
    id: "templates",
    title: "Шаблоны",
    icon: "📝",
    desc: "Генерация документов: ПВК, анкеты, отчёты — на основе актуальных регуляторных требований.",
  },
  {
    id: "profile",
    title: "Биллинг",
    icon: "📊",
    desc: "Управление подпиской, просмотр квоты запросов, история использования.",
  },
  {
    id: "admin",
    title: "Админ",
    icon: "🔒",
    desc: "Модерация заблокированных документов и норм (только для администраторов).",
  },
];

const PIPELINE_STEPS = [
  { icon: "📄", label: "Tier-1 источники" },
  { icon: "🔍", label: "Краулер" },
  { icon: "📝", label: "Парсер" },
  { icon: "🔖", label: "Версионирование" },
  { icon: "⚖️", label: "Извлечение" },
  { icon: "🕸️", label: "Граф" },
  { icon: "📊", label: "Векторный индекс" },
  { icon: "🔎", label: "Поиск" },
  { icon: "✅", label: "Верификация" },
  { icon: "💬", label: "Ответ" },
];

export default function AboutPanel({ onTryDemo, onNavigate }: Props) {
  return (
    <div className="about-panel">
      <section className="about-section intro-section">
        <h2>ИИ помощник по ПОД/ФТ/ФРОМУ</h2>
        <p className="about-subtitle">
          Extractive RAG-платформа для комплаенс-проверки и получения информации
          по противодействию легализации доходов и финансированию терроризма.
        </p>
        <div className="about-highlights">
          <span className="highlight-badge">✓ Только Tier-1 источники</span>
          <span className="highlight-badge">✓ Цитирование параграфов</span>
          <span className="highlight-badge">✓ Evidence trail</span>
          <span className="highlight-badge">✓ Extractive RAG</span>
        </div>
      </section>

      <section className="about-section">
        <h3>Схема работы</h3>
        <div className="pipeline-schema">
          {PIPELINE_STEPS.map((step, i) => (
            <div className="pipeline-step" key={i}>
              <span className="pipeline-icon">{step.icon}</span>
              <span className="pipeline-label">{step.label}</span>
              {i < PIPELINE_STEPS.length - 1 && (
                <span className="pipeline-arrow">→</span>
              )}
            </div>
          ))}
        </div>
      </section>

      <section className="about-section">
        <h3>Все возможности</h3>
        <div className="features-grid">
          {FEATURES.map((f) => (
            <div className="feature-card" key={f.id}>
              <span className="feature-icon">{f.icon}</span>
              <div className="feature-body">
                <h4>{f.title}</h4>
                <p>{f.desc}</p>
                <button
                  className="btn-feature"
                  onClick={() => onNavigate(f.id)}
                >
                  Перейти
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="about-section demo-section">
        <h3>Попробовать</h3>
        <p className="demo-desc">
          Нажмите кнопку ниже, чтобы перейти к запросу с готовым примером:
        </p>
        <div className="demo-box">
          <p className="demo-question">{DEMO_QUESTION}</p>
          <button className="btn-demo" onClick={() => onTryDemo(DEMO_QUESTION)}>
            Попробовать
          </button>
        </div>
      </section>

      <section className="about-section contact-section">
        <h3>О проекте</h3>
        <p>
          Система использует extractive RAG: ответы формируются исключительно на
          основе официальных регуляторных источников Tier-1
          (Росфинмониторинг, Банк России, официальное опубликование).
          Каждый ответ сопровождается цитированием конкретных параграфов
          и полным evidence trail (источник, версия, фрагмент, промпт,
          решение верификатора).
        </p>
      </section>
    </div>
  );
}
