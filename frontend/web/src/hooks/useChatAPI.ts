import { askQuestion as apiAskQuestion, type CitationLabel } from "../api";
import type { ChatSession, Message } from "./useChat";

const API_BASE = "/api/v1";

export async function createChatSession(title?: string): Promise<ChatSession | null> {
  try {
    const res = await fetch(`${API_BASE}/chat/sessions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title || null, tenant_id: "web" }),
    });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export async function listChatSessions(): Promise<ChatSession[]> {
  try {
    const res = await fetch(`${API_BASE}/chat/sessions?tenant_id=web`);
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export async function fetchChatMessages(sessionId: string): Promise<Message[]> {
  try {
    const res = await fetch(`${API_BASE}/chat/sessions/${sessionId}/messages`);
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export async function submitFeedback(
  sessionId: string,
  messageId: string,
  rating: number,
  comment?: string,
): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/chat/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message_id: messageId, rating, comment: comment || null }),
    });
    return res.ok;
  } catch {
    return false;
  }
}

export async function streamAnswer(
  sessionId: string,
  onToken: (token: string) => void,
  onCitations: (citations: CitationLabel[]) => void,
  onDone: () => void,
  onError: (err: string) => void,
): Promise<AbortController> {
  const controller = new AbortController();

  try {
    const res = await fetch(`${API_BASE}/answer/${sessionId}/stream`, {
      signal: controller.signal,
    });
    if (!res.ok) {
      onError(`HTTP ${res.status}`);
      return controller;
    }

    const reader = res.body?.getReader();
    if (!reader) {
      onError("No response body");
      return controller;
    }

    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = line.slice(6).trim();
        if (data === "[DONE]") {
          onDone();
          continue;
        }
        try {
          const parsed = JSON.parse(data);
          if (parsed.type === "token") {
            onToken(parsed.text);
          } else if (parsed.type === "citations") {
            onCitations(parsed.citations);
          } else if (parsed.type === "error") {
            onError(parsed.reason_code || "Unknown error");
          }
        } catch {
          // skip malformed JSON
        }
      }
    }
    onDone();
  } catch (err: unknown) {
    if (err instanceof Error && err.name !== "AbortError") {
      onError(err.message);
    }
  }

  return controller;
}

export { apiAskQuestion };
