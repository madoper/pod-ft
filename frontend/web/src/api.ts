const API_BASE = "/api/v1";

export interface CitationLabel {
  label: string;
  text: string;
  source: string;
  version?: string;
}

export interface AnswerResponse {
  answer: string;
  evidence: CitationLabel[];
}

export interface CheckResponse {
  job_id: string;
  status: string;
}

export interface CheckResult {
  status: string;
  result?: {
    total_fragments_found: number;
    fragments: Array<{
      label: string;
      text: string;
      status: string;
    }>;
  };
  error_message?: string;
}

export async function askQuestion(
  question: string,
  subjectType?: string,
): Promise<AnswerResponse> {
  const res = await fetch(`${API_BASE}/answer`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      subject_type: subjectType || "credit_organization",
      channel: "web",
    }),
  });
  if (!res.ok) {
    const err = await res.text().catch(() => "Unknown error");
    throw new Error(`HTTP ${res.status}: ${err}`);
  }
  return res.json();
}

export async function submitCheck(
  documentText: string,
  documentTitle: string,
  documentType: string,
): Promise<CheckResponse> {
  const res = await fetch(`${API_BASE}/check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tenant_id: "web",
      document_text: documentText,
      document_title: documentTitle,
      document_type: documentType,
      subject_type: "credit_organization",
    }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function pollCheckResult(jobId: string): Promise<CheckResult> {
  const res = await fetch(`${API_BASE}/check/${jobId}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

export async function fetchSources(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/sources`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.sources || [];
}

export interface BlockedItem {
  id: string;
  type: "document" | "norm";
  reason: string;
  blocked_at: string;
}

export async function fetchAdminBlocks(): Promise<BlockedItem[]> {
  const res = await fetch(`${API_BASE}/admin/blocks`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.blocks || [];
}

export interface SubscriptionInfo {
  subscription_id: string;
  plan: string;
  queries_used: number;
  queries_limit: number;
  expires_at: string;
}

export async function fetchSubscription(userId: string): Promise<SubscriptionInfo | null> {
  const res = await fetch(`${API_BASE}/billing/subscription/${userId}`);
  if (!res.ok) return null;
  return res.json();
}

export async function fetchQuota(userId: string): Promise<any | null> {
  const res = await fetch(`${API_BASE}/billing/quota/${userId}`);
  if (!res.ok) return null;
  return res.json();
}
