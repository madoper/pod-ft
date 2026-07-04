import { useState, useEffect } from "react";
import type { CitationLabel } from "./api";
import QuestionPanel from "./components/QuestionPanel";
import AnswerPanel from "./components/AnswerPanel";
import DashboardPanel from "./components/DashboardPanel";
import DocCheckPanel from "./components/DocCheckPanel";
import SourcePanel from "./components/SourcePanel";
import DocumentsPanel from "./components/DocumentsPanel";
import ChangesPanel from "./components/ChangesPanel";
import SubjectProfilePanel from "./components/SubjectProfilePanel";
import TemplatesPanel from "./components/TemplatesPanel";
import AdminPanel from "./components/AdminPanel";
import ProfilePanel from "./components/ProfilePanel";
import AboutPanel from "./components/AboutPanel";
import OnboardingGuide from "./components/OnboardingGuide";

type Tab = "about" | "ask" | "check" | "sources" | "documents" | "changes" | "profile" | "subject-profile" | "templates" | "admin" | "dashboard";

const STORAGE_KEY = "podft_onboarding_seen";
const GUIDE_KEY = "podft_guide_completed";

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState<CitationLabel[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showWelcome, setShowWelcome] = useState(false);
  const [demoQuestion, setDemoQuestion] = useState<string | null>(null);
  const [showGuide, setShowGuide] = useState(false);

  useEffect(() => {
    const seen = localStorage.getItem(STORAGE_KEY);
    if (!seen) setShowWelcome(true);
  }, []);

  function handleDismissWelcome() {
    setShowWelcome(false);
    localStorage.setItem(STORAGE_KEY, "true");
  }

  function handleWelcomeAbout() {
    handleDismissWelcome();
    setTab("about");
  }

  function handleWelcomeStart() {
    handleDismissWelcome();
    const guideSeen = localStorage.getItem(GUIDE_KEY);
    if (!guideSeen) {
      setTab("ask");
      setShowGuide(true);
    } else {
      setTab("ask");
    }
  }

  function handleGuideComplete() {
    setShowGuide(false);
    localStorage.setItem(GUIDE_KEY, "true");
  }

  function handleTryDemo(question: string) {
    setDemoQuestion(question);
    setTab("ask");
  }

  function handleNavigate(target: string) {
    setTab(target as Tab);
  }

  return (
    <div className="app">
      <header>
        <h1>ИИ помощник по ПОД/ФТ/ФРОМУ</h1>
        <nav>
          <button className={tab === "about" ? "active" : ""} onClick={() => setTab("about")}>
            О проекте
          </button>
          <button className={tab === "dashboard" ? "active" : ""} onClick={() => setTab("dashboard")}>
            Дашборд
          </button>
          <button className={tab === "ask" ? "active" : ""} onClick={() => setTab("ask")}>
            Запрос
          </button>
          <button className={tab === "check" ? "active" : ""} onClick={() => setTab("check")}>
            Проверка
          </button>
          <button className={tab === "sources" ? "active" : ""} onClick={() => setTab("sources")}>
            Источники
          </button>
          <button className={tab === "documents" ? "active" : ""} onClick={() => setTab("documents")}>
            Каталог
          </button>
          <button className={tab === "changes" ? "active" : ""} onClick={() => setTab("changes")}>
            Изменения
          </button>
          <button className={tab === "profile" ? "active" : ""} onClick={() => setTab("profile")}>
            Биллинг
          </button>
          <button className={tab === "subject-profile" ? "active" : ""} onClick={() => setTab("subject-profile")}>
            Профиль
          </button>
          <button className={tab === "templates" ? "active" : ""} onClick={() => setTab("templates")}>
            Шаблоны
          </button>
          <button className={tab === "admin" ? "active" : ""} onClick={() => setTab("admin")}>
            Админ
          </button>
        </nav>
      </header>

      <main>
        {tab === "about" && (
          <AboutPanel onTryDemo={handleTryDemo} onNavigate={handleNavigate} />
        )}
        {tab === "dashboard" && <DashboardPanel />}
        {tab === "ask" && (
          <div className="two-panel">
            <QuestionPanel
              key={demoQuestion || "default"}
              initialQuestion={demoQuestion || undefined}
              onAnswer={(a, e) => { setAnswer(a); setEvidence(e); setError(""); }}
              onError={(e) => { setError(e); setAnswer(""); setEvidence([]); }}
              loading={loading}
              setLoading={setLoading}
            />
            <AnswerPanel answer={answer} evidence={evidence} loading={loading} error={error} />
          </div>
        )}
        {tab === "check" && <DocCheckPanel />}
        {tab === "sources" && <SourcePanel />}
        {tab === "documents" && <DocumentsPanel />}
        {tab === "changes" && <ChangesPanel />}
        {tab === "profile" && <ProfilePanel />}
        {tab === "subject-profile" && <SubjectProfilePanel />}
        {tab === "templates" && <TemplatesPanel />}
        {tab === "admin" && <AdminPanel />}
      </main>

      {showGuide && (
        <OnboardingGuide
          onComplete={handleGuideComplete}
          onNavigate={handleNavigate}
        />
      )}

      {showWelcome && (
        <div className="modal-overlay" onClick={handleDismissWelcome}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Добро пожаловать!</h2>
            <p>
              ИИ помощник по ПОД/ФТ/ФРОМУ — система комплаенс-проверки на
              основе extractive RAG по официальным регуляторным источникам Tier-1.
            </p>
            <div className="modal-actions">
              <button onClick={handleWelcomeAbout} className="btn-modal-secondary">
                О проекте
              </button>
              <button onClick={handleWelcomeStart} className="btn-modal-primary">
                Начать работу
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
