import type { Message } from "../../hooks/useChat";
import { MessageSquare, Bot } from "lucide-react";

interface ChatHistoryProps {
  messages: Message[];
  streamingText: string;
  streaming: boolean;
}

export default function ChatHistory({ messages, streamingText, streaming }: ChatHistoryProps) {
  return (
    <div role="log" aria-live="polite" aria-label="История сообщений" style={{ flex: 1, overflow: "auto", padding: "var(--spacing-4)", display: "flex", flexDirection: "column", gap: "var(--spacing-4)" }}>
      {messages.length === 0 && !streaming && (
        <div style={{ textAlign: "center", padding: "var(--spacing-10)", color: "var(--color-text-secondary)" }}>
          <MessageSquare size={32} style={{ margin: "0 auto var(--spacing-3)", opacity: 0.5 }} />
          <p style={{ margin: 0, fontSize: "var(--font-size-sm)" }}>
            Задайте вопрос по нормативным документам ПОД/ФТ/ФРОМУ
          </p>
        </div>
      )}

      {messages.map((msg) => (
        <div key={msg.id} style={{ display: "flex", gap: "var(--spacing-3)", alignItems: "flex-start" }}>
          <div
            style={{
              width: "28px",
              height: "28px",
              borderRadius: "var(--radius-sm)",
              background: msg.role === "user" ? "var(--color-primary)" : "var(--color-border)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
              color: msg.role === "user" ? "var(--color-on-primary)" : "var(--color-text-secondary)",
            }}
          >
            {msg.role === "user" ? <MessageSquare size={14} /> : <Bot size={14} />}
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div
              style={{
                background: msg.role === "user" ? "var(--color-primary)" : "var(--card-bg)",
                color: msg.role === "user" ? "var(--color-on-primary)" : "var(--color-text)",
                borderRadius: "var(--radius-md)",
                padding: "var(--spacing-3)",
                fontSize: "var(--font-size-sm)",
                lineHeight: "var(--line-height-body)",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
            >
              {msg.content}
            </div>
            {msg.citations && msg.citations.length > 0 && (
              <div style={{ marginTop: "var(--spacing-2)", display: "flex", flexWrap: "wrap", gap: "var(--spacing-1)" }}>
                {msg.citations.map((c, i) => (
                  <span
                    key={i}
                    style={{
                      padding: "2px var(--spacing-2)",
                      borderRadius: "var(--radius-sm)",
                      border: "1px solid var(--color-border)",
                      fontSize: "var(--font-size-xs)",
                      color: "var(--color-primary)",
                      background: "var(--color-surface)",
                    }}
                    title={c.text}
                  >
                    {c.label || `[${i + 1}]`}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}

      {streaming && (
        <div style={{ display: "flex", gap: "var(--spacing-3)", alignItems: "flex-start" }}>
          <div
            style={{
              width: "28px",
              height: "28px",
              borderRadius: "var(--radius-sm)",
              background: "var(--color-border)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              flexShrink: 0,
              color: "var(--color-text-secondary)",
            }}
          >
            <Bot size={14} />
          </div>
          <div
            style={{
              background: "var(--card-bg)",
              borderRadius: "var(--radius-md)",
              padding: "var(--spacing-3)",
              fontSize: "var(--font-size-sm)",
              lineHeight: "var(--line-height-body)",
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
            }}
          >
            {streamingText}
            <span style={{ animation: "blink 1s infinite", marginLeft: "2px" }}>▍</span>
            <style>{`@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }`}</style>
          </div>
        </div>
      )}
    </div>
  );
}
