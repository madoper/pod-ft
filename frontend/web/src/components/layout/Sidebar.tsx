import { type LucideIcon, BarChart3, MessageSquareText, FileSearch, Library, UserCircle, Settings, Info } from "lucide-react";

type NavItem = {
  id: string;
  label: string;
  icon: LucideIcon;
};

const mainNav: NavItem[] = [
  { id: "superset", label: "Superset", icon: BarChart3 },
  { id: "ask", label: "Запрос", icon: MessageSquareText },
  { id: "check", label: "Проверка", icon: FileSearch },
  { id: "sources", label: "Источники", icon: Library },
  { id: "profile", label: "Профиль", icon: UserCircle },
];

const footerNav: NavItem[] = [
  { id: "about", label: "О проекте", icon: Info },
  { id: "admin", label: "Админ", icon: Settings },
];

interface SidebarProps {
  activeTab: string;
  collapsed: boolean;
  onTabChange: (tab: string) => void;
  onToggleCollapse: () => void;
}

export default function Sidebar({ activeTab, collapsed, onTabChange, onToggleCollapse }: SidebarProps) {
  return (
    <aside
      className="sidebar"
      style={{
        width: collapsed ? "var(--sidebar-collapsed-width)" : "var(--sidebar-width)",
        background: "var(--sidebar-bg)",
        borderRight: "1px solid var(--sidebar-border, var(--color-border))",
        display: "flex",
        flexDirection: "column",
        transition: "width 0.2s",
        overflow: "hidden",
      }}
    >
      <div style={{ padding: "var(--spacing-4)", borderBottom: "1px solid var(--color-border)", display: "flex", alignItems: "center", justifyContent: collapsed ? "center" : "space-between" }}>
        {!collapsed && <span style={{ fontWeight: 700, fontSize: "var(--font-size-lg)", color: "var(--color-primary)" }}>ПОД/ФТ</span>}
        <button
          onClick={onToggleCollapse}
          style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text-secondary)", padding: "var(--spacing-1)", borderRadius: "var(--radius-sm)" }}
          title={collapsed ? "Развернуть" : "Свернуть"}
          aria-label={collapsed ? "Развернуть" : "Свернуть"}
        >
          {collapsed ? "→" : "←"}
        </button>
      </div>

      <nav style={{ flex: 1, display: "flex", flexDirection: "column", padding: "var(--spacing-2)", gap: "2px" }}>
        {mainNav.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              aria-current={isActive ? "page" : undefined}
              title={collapsed ? item.label : undefined}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "var(--spacing-3)",
                padding: collapsed ? "var(--spacing-2)" : "var(--spacing-2) var(--spacing-3)",
                border: "none",
                borderRadius: "var(--radius-md)",
                background: isActive ? "var(--sidebar-active)" : "transparent",
                color: isActive ? "var(--sidebar-active-text)" : "var(--color-text-secondary)",
                cursor: "pointer",
                fontSize: "var(--font-size-sm)",
                fontWeight: isActive ? 600 : 400,
                justifyContent: collapsed ? "center" : "flex-start",
                transition: "background 0.15s",
              }}
              onMouseEnter={(e) => { if (!isActive) e.currentTarget.style.background = "var(--gray-100, #EDEEF2)"; }}
              onMouseLeave={(e) => { if (!isActive) e.currentTarget.style.background = "transparent"; }}
            >
              <Icon size={20} />
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      <div style={{ padding: "var(--spacing-2)", borderTop: "1px solid var(--color-border)", display: "flex", flexDirection: "column", gap: "2px" }}>
        {footerNav.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              aria-current={isActive ? "page" : undefined}
              title={collapsed ? item.label : undefined}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "var(--spacing-3)",
                padding: collapsed ? "var(--spacing-2)" : "var(--spacing-2) var(--spacing-3)",
                border: "none",
                borderRadius: "var(--radius-md)",
                background: isActive ? "var(--sidebar-active)" : "transparent",
                color: isActive ? "var(--sidebar-active-text)" : "var(--color-text-secondary)",
                cursor: "pointer",
                fontSize: "var(--font-size-sm)",
                justifyContent: collapsed ? "center" : "flex-start",
                transition: "background 0.15s",
              }}
            >
              <Icon size={20} />
              {!collapsed && <span>{item.label}</span>}
            </button>
          );
        })}
      </div>
    </aside>
  );
}
