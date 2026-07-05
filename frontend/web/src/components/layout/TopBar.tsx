import { Moon, Sun, Bell, User } from "lucide-react";
import { useThemeContext } from "../ThemeProvider";

interface TopBarProps {
  title?: string;
}

export default function TopBar({ title = "ИИ помощник по ПОД/ФТ/ФРОМУ" }: TopBarProps) {
  const { isDark, toggleTheme } = useThemeContext();

  return (
    <header
      style={{
        height: "var(--topbar-height)",
        background: "var(--topbar-bg)",
        borderBottom: "1px solid var(--topbar-border)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 var(--spacing-6)",
        gap: "var(--spacing-4)",
      }}
    >
      <span style={{ fontWeight: 600, fontSize: "var(--font-size-base)", color: "var(--color-text)" }}>
        {title}
      </span>

      <div style={{ display: "flex", alignItems: "center", gap: "var(--spacing-2)" }}>
        <button
          onClick={toggleTheme}
          aria-label={isDark ? "Светлая тема" : "Тёмная тема"}
          style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text-secondary)", padding: "var(--spacing-2)", borderRadius: "var(--radius-md)" }}
        >
          {isDark ? <Sun size={18} /> : <Moon size={18} />}
        </button>

        <button
          aria-label="Уведомления"
          style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text-secondary)", padding: "var(--spacing-2)", borderRadius: "var(--radius-md)" }}
        >
          <Bell size={18} />
        </button>

        <div style={{ width: "1px", height: "24px", background: "var(--color-border)", margin: "0 var(--spacing-1)" }} />

        <button
          aria-label="Профиль"
          style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text)", padding: "var(--spacing-2)", borderRadius: "var(--radius-md)", display: "flex", alignItems: "center", gap: "var(--spacing-2)" }}
        >
          <User size={18} />
        </button>
      </div>
    </header>
  );
}
