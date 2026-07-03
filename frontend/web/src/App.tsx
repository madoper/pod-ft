import { useState } from "react";
import type { CitationLabel } from "./api";
import QuestionPanel from "./components/QuestionPanel";
import AnswerPanel from "./components/AnswerPanel";
import DocCheckPanel from "./components/DocCheckPanel";
import SourcePanel from "./components/SourcePanel";
import AdminPanel from "./components/AdminPanel";
import ProfilePanel from "./components/ProfilePanel";

type Tab = "ask" | "check" | "sources" | "admin" | "profile";

export default function App() {
  const [tab, setTab] = useState<Tab>("ask");
  const [answer, setAnswer] = useState("");
  const [evidence, setEvidence] = useState<CitationLabel[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  return (
    <div className="app">
      <header>
        <h1>pod-ft</h1>
        <nav>
          <button className={tab === "ask" ? "active" : ""} onClick={() => setTab("ask")}>
            Задать вопрос
          </button>
          <button className={tab === "check" ? "active" : ""} onClick={() => setTab("check")}>
            Проверка документа
          </button>
          <button className={tab === "sources" ? "active" : ""} onClick={() => setTab("sources")}>
            Источники
          </button>
          <button className={tab === "admin" ? "active" : ""} onClick={() => setTab("admin")}>
            Блокировки
          </button>
          <button className={tab === "profile" ? "active" : ""} onClick={() => setTab("profile")}>
            Профиль
          </button>
        </nav>
      </header>

      <main>
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
        {tab === "admin" && <AdminPanel />}
        {tab === "profile" && <ProfilePanel />}
      </main>
    </div>
  );
}
