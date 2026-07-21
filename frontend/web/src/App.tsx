import { useState, useEffect } from "react";
import { ThemeProvider } from "./components/ThemeProvider";
import AppShell from "./components/layout/AppShell";
import ChatPanel from "./components/chat/ChatPanel";
import DocCheckPanel from "./components/DocCheckPanel";
import SourcePanel from "./components/SourcePanel";
import AboutPanel from "./components/AboutPanel";
import AdminPanel from "./components/AdminPanel";
import ProfilePanel from "./components/ProfilePanel";
import OnboardingGuide from "./components/OnboardingGuide";

type Tab = "ask" | "check" | "sources" | "profile" | "about" | "admin";

const STORAGE_KEY = "podft_onboarding_seen";

export default function App() {
  const [tab, setTab] = useState<Tab>("ask");
  const [showWelcome, setShowWelcome] = useState(false);
  const [showGuide, setShowGuide] = useState(false);

  useEffect(() => {
    const seen = localStorage.getItem(STORAGE_KEY);
    if (!seen) setShowWelcome(true);
  }, []);

  function handleDismissWelcome() {
    setShowWelcome(false);
    localStorage.setItem(STORAGE_KEY, "true");
  }

  function handleTabChange(target: string) {
    setTab(target as Tab);
  }

  return (
    <ThemeProvider>
      <AppShell activeTab={tab} onTabChange={handleTabChange}>
        {tab === "ask" && <ChatPanel />}
        {tab === "check" && <DocCheckPanel />}
        {tab === "sources" && <SourcePanel />}
        {tab === "profile" && <ProfilePanel />}
        {tab === "about" && <AboutPanel onTryDemo={(_q) => { setTab("ask"); }} onNavigate={handleTabChange} />}
        {tab === "admin" && <AdminPanel />}
      </AppShell>

      {showGuide && <OnboardingGuide onComplete={() => { setShowGuide(false); localStorage.setItem("podft_guide_completed", "true"); }} onNavigate={handleTabChange} />}

      {showWelcome && (
        <div
          style={{
            position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000,
          }}
          onClick={handleDismissWelcome}
        >
          <div
            style={{
              background: "var(--card-bg)", borderRadius: "var(--radius-lg)", padding: "var(--spacing-8)", maxWidth: "440px", width: "90%", boxShadow: "0 8px 32px rgba(0,0,0,0.2)",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 style={{ margin: "0 0 var(--spacing-3)" }}>Добро пожаловать!</h2>
            <p style={{ color: "var(--color-text-secondary)", lineHeight: "var(--line-height-body)", margin: 0 }}>
              ИИ помощник по ПОД/ФТ/ФРОМУ — система комплаенс-проверки на основе extractive RAG по официальным регуляторным источникам Tier-1.
            </p>
            <div style={{ display: "flex", gap: "var(--spacing-3)", marginTop: "var(--spacing-6)", justifyContent: "flex-end" }}>
              <button
                onClick={() => { handleDismissWelcome(); setTab("about"); }}
                style={{
                  padding: "var(--spacing-2) var(--spacing-4)", borderRadius: "var(--radius-md)", border: "1px solid var(--color-border)", background: "var(--card-bg)", cursor: "pointer", color: "var(--color-text)", fontSize: "var(--font-size-sm)",
                }}
              >
                О проекте
              </button>
              <button
                onClick={() => {
                  handleDismissWelcome();
                  setTab("ask");
                  const guideSeen = localStorage.getItem("podft_guide_completed");
                  if (!guideSeen) setShowGuide(true);
                }}
                style={{
                  padding: "var(--spacing-2) var(--spacing-4)", borderRadius: "var(--radius-md)", border: "none", background: "var(--color-primary)", color: "var(--color-on-primary)", cursor: "pointer", fontSize: "var(--font-size-sm)", fontWeight: 600,
                }}
              >
                Начать работу
              </button>
            </div>
          </div>
        </div>
      )}
    </ThemeProvider>
  );
}
