import { useState } from "react";

const SUPERSET_URL = "/superset/";

export default function DashboardPanel() {
  const [iframeLoaded, setIframeLoaded] = useState(false);

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", gap: "var(--spacing-4)" }}>
      <h2 style={{ margin: 0, fontSize: "var(--font-size-lg)", color: "var(--color-text)" }}>
        Панель управления
      </h2>
      {!iframeLoaded && (
        <div style={{ padding: "var(--spacing-8)", textAlign: "center", color: "var(--color-text-secondary)" }}>
          Загрузка дашборда...
        </div>
      )}
      <iframe
        src={SUPERSET_URL}
        title="Superset Dashboard"
        onLoad={() => setIframeLoaded(true)}
        style={{
          flex: 1,
          width: "100%",
          border: "none",
          borderRadius: "var(--radius-md)",
          background: "#fff",
          display: iframeLoaded ? "block" : "none",
        }}
        allow="fullscreen"
      />
    </div>
  );
}
