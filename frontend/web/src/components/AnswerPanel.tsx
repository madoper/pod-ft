import type { CitationLabel } from "../api";

interface Props {
  answer: string;
  evidence: CitationLabel[];
  loading: boolean;
  error: string;
}

export default function AnswerPanel({ answer, evidence, loading, error }: Props) {
  if (loading) {
    return (
      <div className="panel answer-panel">
        <h2>Ответ</h2>
        <div className="loading">Ищу ответ...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel answer-panel">
        <h2>Ответ</h2>
        <div className="error">Ошибка: {error}</div>
      </div>
    );
  }

  if (!answer) {
    return (
      <div className="panel answer-panel">
        <h2>Ответ</h2>
        <p className="placeholder">Введите вопрос в левой панели</p>
      </div>
    );
  }

  return (
    <div className="panel answer-panel">
      <h2>Ответ</h2>
      <div className="answer-text">{answer}</div>
      {evidence.length > 0 && (
        <div className="evidence">
          <h3>Источники ({evidence.length})</h3>
          <ul>
            {evidence.map((e, i) => (
              <li key={i} className="citation">
                <strong>{e.label || `Фрагмент ${i + 1}`}</strong>
                <p>{e.text}</p>
                <small>
                  {e.source}
                  {e.version ? ` (${e.version})` : ""}
                </small>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
