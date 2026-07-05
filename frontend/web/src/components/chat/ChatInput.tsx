import { useRef, useEffect } from "react";
import { Send } from "lucide-react";

const QUICK_TEMPLATES = [
  "Какие требования к ПОД/ФТ для кредитных организаций?",
  "Что такое 115-ФЗ?",
  "Какие сроки сообщения в Росфинмониторинг?",
  "Как проводить идентификацию клиента?",
];

interface ChatInputProps {
  value: string;
  onChange: (text: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
}

export default function ChatInput({ value, onChange, onSubmit, disabled }: ChatInputProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = Math.min(ta.scrollHeight, 160) + "px";
    }
  }, [value]);

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onSubmit();
    }
  }

  return (
    <div style={{ padding: "var(--spacing-3)", borderTop: "1px solid var(--input-border)" }}>
      <div style={{ display: "flex", gap: "var(--spacing-2)", flexWrap: "wrap", marginBottom: "var(--spacing-2)" }}>
        {QUICK_TEMPLATES.map((tpl) => (
          <button
            key={tpl}
            onClick={() => onChange(tpl)}
            style={{
              padding: "var(--spacing-1) var(--spacing-2)",
              borderRadius: "var(--radius-sm)",
              border: "1px solid var(--color-border)",
              background: "var(--card-bg)",
              cursor: "pointer",
              fontSize: "var(--font-size-xs)",
              color: "var(--color-text-secondary)",
              whiteSpace: "nowrap",
            }}
          >
            {tpl.length > 30 ? tpl.slice(0, 30) + "…" : tpl}
          </button>
        ))}
      </div>
      <div style={{ display: "flex", gap: "var(--spacing-2)", alignItems: "flex-end" }}>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Задайте вопрос по ПОД/ФТ…"
          disabled={disabled}
          rows={1}
          aria-label="Вопрос"
          style={{
            flex: 1,
            padding: "var(--spacing-2) var(--spacing-3)",
            borderRadius: "var(--radius-md)",
            border: "1px solid var(--input-border)",
            background: "var(--input-bg)",
            color: "var(--color-text)",
            fontSize: "var(--font-size-sm)",
            lineHeight: "var(--line-height-body)",
            resize: "none",
            outline: "none",
            fontFamily: "var(--font-body)",
            minHeight: "40px",
            maxHeight: "160px",
          }}
          onFocus={(e) => { e.currentTarget.style.borderColor = "var(--input-focus)"; }}
          onBlur={(e) => { e.currentTarget.style.borderColor = "var(--input-border)"; }}
        />
        <button
          onClick={onSubmit}
          disabled={disabled || !value.trim()}
          aria-label="Отправить"
          style={{
            padding: "var(--spacing-2)",
            borderRadius: "var(--radius-md)",
            border: "none",
            background: value.trim() && !disabled ? "var(--color-primary)" : "var(--color-border)",
            color: value.trim() && !disabled ? "var(--color-on-primary)" : "var(--color-text-secondary)",
            cursor: value.trim() && !disabled ? "pointer" : "default",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            height: "40px",
            width: "40px",
            flexShrink: 0,
          }}
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}
