import { useState, type ReactNode } from "react";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";
import MobileTabBar from "./MobileTabBar";

interface AppShellProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  children: ReactNode;
}

export default function AppShell({ activeTab, onTabChange, children }: AppShellProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      <Sidebar
        activeTab={activeTab}
        collapsed={collapsed}
        onTabChange={onTabChange}
        onToggleCollapse={() => setCollapsed((c) => !c)}
      />

      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", minWidth: 0 }}>
        <TopBar />

        <main
          style={{
            flex: 1,
            overflow: "auto",
            padding: "var(--spacing-6)",
            background: "var(--color-surface)",
          }}
          className="app-main"
        >
          {children}
        </main>
      </div>

      <MobileTabBar activeTab={activeTab} onTabChange={onTabChange} />
    </div>
  );
}
