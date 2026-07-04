import { useState } from "react";

interface Step {
  title: string;
  description: string;
  targetTab: string;
  icon: string;
}

const STEPS: Step[] = [
  {
    title: "Задайте вопрос",
    description: "Введите вопрос по ПОД/ФТ/ФРОМУ — система найдёт ответ в официальных регуляторных источниках Tier-1 с цитированием конкретных параграфов и полным evidence trail.",
    targetTab: "ask",
    icon: "💬",
  },
  {
    title: "Проверьте документы",
    description: "Загрузите внутренний документ (ПВК, анкету, отчёт) — система проверит его на соответствие актуальным требованиям и укажет недостающие нормы.",
    targetTab: "check",
    icon: "📋",
  },
  {
    title: "Изучайте источники",
    description: "Просматривайте активные регуляторные источники, их статус и историю изменений. Все источники Tier-1 проходят автоматический мониторинг.",
    targetTab: "sources",
    icon: "📚",
  },
  {
    title: "Следите за изменениями",
    description: "Мониторинг изменений в регуляторной базе: новые документы, обновления обязательств, история версий.",
    targetTab: "changes",
    icon: "🔄",
  },
  {
    title: "Всё готово!",
    description: "Теперь вы можете пользоваться всеми возможностями системы. При необходимости вернитесь к обучению через раздел «О проекте».",
    targetTab: "",
    icon: "🎉",
  },
];

interface Props {
  onComplete: () => void;
  onNavigate: (tab: string) => void;
}

export default function OnboardingGuide({ onComplete, onNavigate }: Props) {
  const [step, setStep] = useState(0);

  function handleNext() {
    const next = step + 1;
    if (next >= STEPS.length) {
      onComplete();
      return;
    }
    const s = STEPS[next];
    if (s.targetTab) onNavigate(s.targetTab);
    setStep(next);
  }

  function handlePrev() {
    if (step <= 0) return;
    const prev = step - 1;
    const s = STEPS[prev];
    if (s.targetTab) onNavigate(s.targetTab);
    setStep(prev);
  }

  const current = STEPS[step];
  const isLast = step >= STEPS.length - 1;

  return (
    <div className="guide-overlay">
      <div className="guide-card">
        <div className="guide-steps">
          {STEPS.map((_, i) => (
            <div key={i} className={`guide-dot${i === step ? " active" : ""}${i < step ? " done" : ""}`} />
          ))}
        </div>
        <div className="guide-icon">{current.icon}</div>
        <h3 className="guide-title">{current.title}</h3>
        <p className="guide-desc">{current.description}</p>
        <div className="guide-actions">
          {step > 0 && (
            <button className="btn-guide-prev" onClick={handlePrev}>Назад</button>
          )}
          <button className="btn-guide-next" onClick={handleNext}>
            {isLast ? "Завершить" : "Далее"}
          </button>
        </div>
        {!isLast && (
          <button className="btn-guide-skip" onClick={onComplete}>Пропустить</button>
        )}
      </div>
    </div>
  );
}
