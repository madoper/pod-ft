import { BarChart3, MessageSquareText, FileSearch, Library, UserCircle } from "lucide-react";

interface MobileTabBarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

const tabs = [
  { id: "superset", label: "Superset", icon: BarChart3 },
  { id: "ask", label: "Запрос", icon: MessageSquareText },
  { id: "check", label: "Проверка", icon: FileSearch },
  { id: "sources", label: "Источники", icon: Library },
  { id: "profile", label: "Профиль", icon: UserCircle },
];

export default function MobileTabBar({ activeTab, onTabChange }: MobileTabBarProps) {
  return (
    <nav
      style={{
        display: "none",
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        height: "56px",
        background: "var(--sidebar-bg)",
        borderTop: "1px solid var(--color-border)",
        zIndex: 100,
        justifyContent: "space-around",
        alignItems: "center",
      }}
      className="mobile-tab-bar"
    >
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            aria-label={tab.label}
            aria-current={isActive ? "page" : undefined}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "2px",
              background: "none",
              border: "none",
              cursor: "pointer",
              color: isActive ? "var(--sidebar-active-text)" : "var(--color-text-secondary)",
              fontSize: "10px",
              padding: "var(--spacing-1)",
            }}
          >
            <Icon size={20} />
            <span>{tab.label}</span>
          </button>
        );
      })}
    </nav>
  );
}
