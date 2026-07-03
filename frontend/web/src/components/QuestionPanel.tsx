import { useState, type FormEvent } from "react";
import type { CitationLabel } from "./api";

interface Props {
  onAnswer: (answer: string, evidence: CitationLabel[]) => void;
  onError: (error: string) => void;
  loading: boolean;
  setLoading: (v: boolean) => void;
}

export default function QuestionPanel({
  onAnswer,
  onError,
  loading,
  setLoading,
}: Props) {
  const [question, setQuestion] = useState("");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const q = question.trim();
    if (!q || loading) return;

    setLoading(true);
    onAnswer("", []);
    try {
      const { askQuestion } = await import("./api");
      const data = await askQuestion(q);
      onAnswer(data.answer, data.evidence);
    } catch (err: any) {
      onError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="panel question-panel">
      <h2>Запрос</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Введите вопрос по ПОД/ФТ/ФРОМУ..."
          rows={4}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !question.trim()}>
          {loading ? "Поиск..." : "Задать вопрос"}
        </button>
      </form>
    </div>
  );
}
