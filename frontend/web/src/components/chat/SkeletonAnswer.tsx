export default function SkeletonAnswer() {
  return (
    <div role="status" aria-label="Загрузка ответа" style={{ display: "flex", flexDirection: "column", gap: "var(--spacing-3)", padding: "var(--spacing-4)" }}>
      <div aria-hidden="true" style={{ height: "16px", width: "70%", background: "var(--color-border)", borderRadius: "var(--radius-sm)", animation: "pulse 1.5s infinite" }} />
      <div aria-hidden="true" style={{ height: "16px", width: "90%", background: "var(--color-border)", borderRadius: "var(--radius-sm)", animation: "pulse 1.5s infinite 0.2s" }} />
      <div aria-hidden="true" style={{ height: "16px", width: "60%", background: "var(--color-border)", borderRadius: "var(--radius-sm)", animation: "pulse 1.5s infinite 0.4s" }} />
      <div aria-hidden="true" style={{ height: "80px", width: "100%", background: "var(--color-border)", borderRadius: "var(--radius-md)", animation: "pulse 1.5s infinite 0.6s" }} />
      <div aria-hidden="true" style={{ height: "80px", width: "100%", background: "var(--color-border)", borderRadius: "var(--radius-md)", animation: "pulse 1.5s infinite 0.8s" }} />
      <style>{`@keyframes pulse { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }`}</style>
    </div>
  );
}
