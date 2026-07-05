import type { CitationLabel } from "../api";

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: CitationLabel[];
};

export type ChatSession = {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
};

export type ChatState = {
  sessions: ChatSession[];
  activeSessionId: string | null;
  messages: Message[];
  streaming: boolean;
  streamingText: string;
  error: string | null;
  inputText: string;
};

export type ChatAction =
  | { type: "SET_SESSIONS"; sessions: ChatSession[] }
  | { type: "SET_ACTIVE_SESSION"; sessionId: string | null }
  | { type: "SET_MESSAGES"; messages: Message[] }
  | { type: "ADD_USER_MESSAGE"; message: Message }
  | { type: "START_STREAMING" }
  | { type: "STREAM_TOKEN"; text: string }
  | { type: "FINISH_STREAMING"; citations?: CitationLabel[] }
  | { type: "SET_ERROR"; error: string }
  | { type: "SET_INPUT"; text: string }
  | { type: "ADD_SESSION"; session: ChatSession };

export const initialChatState: ChatState = {
  sessions: [],
  activeSessionId: null,
  messages: [],
  streaming: false,
  streamingText: "",
  error: null,
  inputText: "",
};

export function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case "SET_SESSIONS":
      return { ...state, sessions: action.sessions };
    case "SET_ACTIVE_SESSION":
      return { ...state, activeSessionId: action.sessionId };
    case "SET_MESSAGES":
      return { ...state, messages: action.messages };
    case "ADD_USER_MESSAGE":
      return { ...state, messages: [...state.messages, action.message] };
    case "START_STREAMING":
      return { ...state, streaming: true, streamingText: "", error: null };
    case "STREAM_TOKEN":
      return { ...state, streamingText: state.streamingText + action.text };
    case "FINISH_STREAMING": {
      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: state.streamingText,
        citations: action.citations,
      };
      return {
        ...state,
        messages: [...state.messages, assistantMsg],
        streaming: false,
        streamingText: "",
      };
    }
    case "SET_ERROR":
      return { ...state, error: action.error, streaming: false, streamingText: "" };
    case "SET_INPUT":
      return { ...state, inputText: action.text };
    case "ADD_SESSION":
      return { ...state, sessions: [action.session, ...state.sessions] };
    default:
      return state;
  }
}
