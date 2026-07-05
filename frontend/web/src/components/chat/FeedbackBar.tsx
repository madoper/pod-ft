import { ThumbsUp, ThumbsDown } from "lucide-react";
import { submitFeedback } from "../../hooks/useChatAPI";

interface FeedbackBarProps {
  sessionId: string;
  messageId: string;
  onFeedbackSubmitted?: () => void;
}

export default function FeedbackBar({ sessionId, messageId, onFeedbackSubmitted }: FeedbackBarProps) {
  async function handleFeedback(rating: number) {
    await submitFeedback(sessionId, messageId, rating);
    onFeedbackSubmitted?.();
  }

  return (
    <div style={{ display: "flex", alignItems: "center", gap: "var(--spacing-2)", marginTop: "var(--spacing-2)" }}>
      <span style={{ fontSize: "var(--font-size-xs)", color: "var(--color-text-secondary)" }}>Ответ полезен?</span>
      <button
        onClick={() => handleFeedback(1)}
        aria-label="Полезно"
        style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text-secondary)", padding: "var(--spacing-1)", borderRadius: "var(--radius-sm)" }}
      >
        <ThumbsUp size={14} />
      </button>
      <button
        onClick={() => handleFeedback(-1)}
        aria-label="Не полезно"
        style={{ background: "none", border: "none", cursor: "pointer", color: "var(--color-text-secondary)", padding: "var(--spacing-1)", borderRadius: "var(--radius-sm)" }}
      >
        <ThumbsDown size={14} />
      </button>
    </div>
  );
}
