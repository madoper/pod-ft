const API_BASE = "/api/v1";

export interface CitationLabel {
  label: string;
  text: string;
  source: string;
  version?: string;
  confidenceScore?: number;
}

export interface AnswerResponse {
  answer: string;
  evidence: CitationLabel[];
  answer_session_id?: string;
  status?: string;
  evidence_count?: number;
  verifier_status?: string;
  llmSummary?: string | null;
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
  const data = await res.json();
  const summary = data.answer?.summary || "";
  const citations = data.answer?.citations || [];
  const evidence: CitationLabel[] = citations.map((c: any) => ({
    label: c.citation_label || "",
    text: c.quote || "",
    source: c.document_title || c.source_url || "",
    version: c.version_effective_from || undefined,
    confidenceScore: c.confidence_score ?? undefined,
  }));
  return {
    answer: summary,
    evidence,
    answer_session_id: data.answer_session_id,
    status: data.status,
    evidence_count: data.evidence_count,
    verifier_status: data.verifier_status,
    llmSummary: data.answer?.llm_summary ?? null,
  };
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

export interface FindingData {
  finding_type: string;
  summary: string;
  obligation_id?: string;
  citation_label?: string;
  fragment_text?: string;
  confidence: number;
}

export interface ExportLinkData {
  format: string;
  url: string;
  label: string;
}

export interface CheckResultData {
  job_id: string;
  status: string;
  total_fragments_found: number;
  findings: FindingData[];
  coverage_summary: string;
  created_at: string;
  export_links: ExportLinkData[];
}

export async function getCheckResult(jobId: string): Promise<CheckResultData | null> {
  const res = await fetch(`${API_BASE}/check/${jobId}`);
  if (!res.ok) return null;
  const data = await res.json();
  if (data.status !== "completed" || !data.result) return null;
  return data.result as CheckResultData;
}

export async function fetchSources(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/sources/active`);
  if (!res.ok) return [];
  const data = await res.json();
  return Array.isArray(data) ? data : data.sources || [];
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
  tenant_id: string;
  tier: string;
  monthly_quota: number;
  usage_this_month: number;
  quota_remaining: number;
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

export interface SourceItem {
  id: string;
  domain: string;
  source_type: string;
  regulator_name: string;
  tier: number;
  is_active: boolean;
}

export async function fetchSourcesDetail(): Promise<SourceItem[]> {
  const res = await fetch(`${API_BASE}/sources/active`);
  if (!res.ok) return [];
  const data = await res.json();
  return Array.isArray(data) ? data : data.sources || [];
}

export interface ChangeItem {
  document_id: string;
  title: string;
  version_label: string;
  change_type: string;
  effective_from?: string;
  summary?: string;
}

export async function fetchChanges(fromDate?: string): Promise<ChangeItem[]> {
  const params = fromDate ? `?from_date=${fromDate}` : "";
  const res = await fetch(`${API_BASE}/changes${params}`);
  if (!res.ok) return [];
  return res.json().then((d) => d.changes || d.items || []);
}

export interface SubjectProfileDto {
  id?: string;
  subject_type: string;
  regulator?: string;
  extra_criteria?: Record<string, unknown>;
  created_at?: string;
}

export async function fetchProfiles(tenantId: string): Promise<SubjectProfileDto[]> {
  const res = await fetch(`${API_BASE}/tenant-profile/by-tenant/${tenantId}`);
  if (!res.ok) return [];
  const data = await res.json();
  return data.profiles || [];
}

export async function createProfile(
  tenantId: string,
  subjectType: string,
  regulator?: string,
): Promise<SubjectProfileDto | null> {
  const res = await fetch(`${API_BASE}/tenant-profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tenant_id: tenantId, subject_type: subjectType, regulator }),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function deleteProfile(profileId: string): Promise<boolean> {
  const res = await fetch(`${API_BASE}/tenant-profile/${profileId}`, { method: "DELETE" });
  return res.ok;
}

export interface TemplateInfo {
  draft_id: string;
  document_type: string;
  title: string;
  summary: string;
}

export async function fetchTemplates(): Promise<TemplateInfo[]> {
  const res = await fetch(`${API_BASE}/drafts`);
  if (!res.ok) return [];
  const data = await res.json();
  return Array.isArray(data) ? data : [];
}

export async function fetchUsageStats(): Promise<any> {
  return { queries_today: 0, queries_this_month: 0, sources_count: 0, documents_count: 0 };
}
