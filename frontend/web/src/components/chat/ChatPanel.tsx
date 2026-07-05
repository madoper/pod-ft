import { useCallback, useEffect, useReducer, useRef } from "react";
import type { CitationLabel } from "../../api";

declare global {
  interface Window {
    __streamCitations?: CitationLabel[];
  }
}
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

    // Create session if none active
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

    // Add user message
    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };
    dispatch({ type: "ADD_USER_MESSAGE", message: userMsg });

    // Start streaming
    dispatch({ type: "START_STREAMING" });

    // Call the answer API to trigger processing
    try {
      const answerRes = await apiAskQuestion(question);
      if (answerRes.status === "refused") {
        dispatch({ type: "STREAM_TOKEN", text: answerRes.answer || "Недостаточно данных для ответа." });
        dispatch({ type: "FINISH_STREAMING", citations: [] });
        return;
      }

      // Stream the result
      const controller = await streamAnswer(
        sessionId,
        (token) => dispatch({ type: "STREAM_TOKEN", text: token }),
        (citations) => {
          // Store citations for later
          window.__streamCitations = citations;
        },
        () => {
          const citations = (window as any).__streamCitations || answerRes.evidence || [];
          dispatch({ type: "FINISH_STREAMING", citations });
          (window as any).__streamCitations = undefined;
        },
        (err) => dispatch({ type: "SET_ERROR", error: err }),
      );
      abortRef.current = controller;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      dispatch({ type: "SET_ERROR", error: msg });
    }
  }, [state.inputText, state.streaming, state.activeSessionId]);

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
