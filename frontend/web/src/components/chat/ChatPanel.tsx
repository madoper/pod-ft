import { useCallback, useEffect, useReducer, useRef } from "react";
import { chatReducer, initialChatState, type Message } from "../../hooks/useChat";
import {
  createChatSession,
  listChatSessions,
  fetchChatMessages,
  streamAnswer,
  apiAskQuestion,
} from "../../hooks/useChatAPI";
import ChatHistory from "./ChatHistory";
import ChatInput from "./ChatInput";

export default function ChatPanel() {
  const [state, dispatch] = useReducer(chatReducer, initialChatState);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    listChatSessions().then((sessions) => {
      dispatch({ type: "SET_SESSIONS", sessions });
      if (sessions.length > 0 && !state.activeSessionId) {
        dispatch({ type: "SET_ACTIVE_SESSION", sessionId: sessions[0].id });
        fetchChatMessages(sessions[0].id).then((msgs) => {
          dispatch({ type: "SET_MESSAGES", messages: msgs });
        });
      }
    });
  }, []);

  const handleSubmit = useCallback(async () => {
    const question = state.inputText.trim();
    if (!question || state.streaming) return;

    dispatch({ type: "SET_INPUT", text: "" });

    let sessionId = state.activeSessionId;

    if (!sessionId) {
      const session = await createChatSession(question.slice(0, 50));
      if (session) {
        sessionId = session.id;
        dispatch({ type: "ADD_SESSION", session });
        dispatch({ type: "SET_ACTIVE_SESSION", sessionId: session.id });
      } else {
        dispatch({ type: "SET_ERROR", error: "Failed to create session" });
        return;
      }
    }

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };
    dispatch({ type: "ADD_USER_MESSAGE", message: userMsg });
    dispatch({ type: "START_STREAMING" });

    try {
      const answerRes = await apiAskQuestion(question);
      if (answerRes.status === "refused") {
        dispatch({ type: "STREAM_TOKEN", text: answerRes.answer || "Недостаточно данных для ответа." });
        dispatch({ type: "FINISH_STREAMING", citations: [] });
        return;
      }

      const ansSessionId = answerRes.answer_session_id;
      if (!ansSessionId) {
        dispatch({ type: "SET_ERROR", error: "No answer session ID" });
        return;
      }

      const controller = await streamAnswer(
        ansSessionId,
        (token) => dispatch({ type: "STREAM_TOKEN", text: token }),
        (citations) => {
          const msgs = state.messages;
          const last = msgs[msgs.length - 1];
          if (last && last.role === "assistant") {
            last.citations = citations as any;
          }
        },
        () => {
          const citations = answerRes.evidence || [];
          dispatch({ type: "FINISH_STREAMING", citations });
        },
        (err) => dispatch({ type: "SET_ERROR", error: err }),
      );
      abortRef.current = controller;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      dispatch({ type: "SET_ERROR", error: msg });
    }
  }, [state.inputText, state.streaming, state.activeSessionId, state.messages]);

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", background: "var(--color-surface)", borderRadius: "var(--radius-lg)", overflow: "hidden", border: "1px solid var(--color-border)" }}>
      <ChatHistory
        messages={state.messages}
        streamingText={state.streamingText}
        streaming={state.streaming}
      />
      {state.error && (
        <div style={{ padding: "var(--spacing-2) var(--spacing-4)", background: "var(--color-danger)", color: "#fff", fontSize: "var(--font-size-xs)" }}>
          {state.error}
        </div>
      )}
      <ChatInput
        value={state.inputText}
        onChange={(text) => dispatch({ type: "SET_INPUT", text })}
        onSubmit={handleSubmit}
        disabled={state.streaming}
      />
    </div>
  );
}
