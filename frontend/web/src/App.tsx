import { useState } from "react";
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

type Tab = "ask" | "check" | "sources" | "documents" | "changes" | "profile" | "subject-profile" | "templates" | "admin" | "dashboard";

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState<CitationLabel[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <div className="app">
      <header>
        <h1>pod-ft</h1>
        <nav>
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
        {tab === "dashboard" && <DashboardPanel />}
        {tab === "ask" && (
          <div className="two-panel">
            <QuestionPanel
              onAnswer={(a, e) => {
                setAnswer(a);
                setEvidence(e);
                setError("");
              }}
              onError={(e) => {
                setError(e);
                setAnswer("");
                setEvidence([]);
              }}
              loading={loading}
              setLoading={setLoading}
            />
            <AnswerPanel
              answer={answer}
              evidence={evidence}
              loading={loading}
              error={error}
            />
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
    </div>
  );
}
