-- pod-ft: PostgreSQL initialization
-- schema-ref: project-schema.yaml#/databases/postgres

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- tenants
CREATE TABLE IF NOT EXISTS tenants (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                TEXT NOT NULL UNIQUE,
    display_name        TEXT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'active',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- users
CREATE TABLE IF NOT EXISTS users (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    email               TEXT NOT NULL UNIQUE,
    password_hash       TEXT NOT NULL,
    role                TEXT NOT NULL DEFAULT 'user',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- subscriptions
CREATE TABLE IF NOT EXISTS subscriptions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    tier                TEXT NOT NULL DEFAULT 'free',
    monthly_quota       INTEGER NOT NULL DEFAULT 100,
    starts_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    ends_at             TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- usage_ledger
CREATE TABLE IF NOT EXISTS usage_ledger (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    event_type          TEXT NOT NULL,
    tokens_used         INTEGER NOT NULL DEFAULT 0,
    cost                NUMERIC(12,6) NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- source_domains
CREATE TABLE IF NOT EXISTS source_domains (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain              TEXT NOT NULL UNIQUE,
    source_type         TEXT NOT NULL,
    regulator_name      TEXT NOT NULL,
    tier                SMALLINT NOT NULL,
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- source_endpoints
CREATE TABLE IF NOT EXISTS source_endpoints (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_id           UUID NOT NULL REFERENCES source_domains(id) ON DELETE CASCADE,
    url_pattern         TEXT NOT NULL,
    crawl_frequency     TEXT NOT NULL DEFAULT 'daily',
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- crawl_jobs
CREATE TABLE IF NOT EXISTS crawl_jobs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    endpoint_id         UUID NOT NULL REFERENCES source_endpoints(id) ON DELETE CASCADE,
    status              TEXT NOT NULL DEFAULT 'queued',
    started_at          TIMESTAMPTZ,
    completed_at        TIMESTAMPTZ,
    error_message       TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- crawl_results
CREATE TABLE IF NOT EXISTS crawl_results (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id              UUID NOT NULL REFERENCES crawl_jobs(id) ON DELETE CASCADE,
    url                 TEXT NOT NULL,
    content_type        TEXT,
    blob_key            TEXT NOT NULL,
    checksum            TEXT NOT NULL,
    discovered_at       TIMESTAMPTZ NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- documents
CREATE TABLE IF NOT EXISTS documents (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_domain_id    UUID NOT NULL REFERENCES source_domains(id),
    canonical_url       TEXT NOT NULL UNIQUE,
    title               TEXT,
    document_kind       TEXT NOT NULL,
    regulator_code      TEXT,
    official_number     TEXT,
    official_date       DATE,
    status              TEXT NOT NULL DEFAULT 'active',
    first_seen_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- document_versions
CREATE TABLE IF NOT EXISTS document_versions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id         UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    version_label       TEXT,
    effective_from      DATE,
    effective_to        DATE,
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    content_hash        TEXT NOT NULL,
    source_blob_key     TEXT NOT NULL,
    parsed_text_blob_key TEXT,
    parse_status        TEXT NOT NULL DEFAULT 'pending',
    ocr_used            BOOLEAN NOT NULL DEFAULT FALSE,
    superseded_by_id    UUID NULL REFERENCES document_versions(id),
    is_current          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(document_id, content_hash)
);

-- document_fragments
CREATE TABLE IF NOT EXISTS document_fragments (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_version_id UUID NOT NULL REFERENCES document_versions(id) ON DELETE CASCADE,
    fragment_no         INTEGER NOT NULL,
    section_path        TEXT,
    paragraph_label     TEXT,
    page_no             INTEGER,
    fragment_text       TEXT NOT NULL,
    canonical_text      TEXT NOT NULL,
    token_count         INTEGER,
    extraction_confidence NUMERIC(5,4),
    citation_label      TEXT NOT NULL,
    fragment_hash       TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(document_version_id, fragment_no)
);

-- norms
CREATE TABLE IF NOT EXISTS norms (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    norm_code           TEXT UNIQUE,
    title               TEXT,
    norm_type           TEXT NOT NULL,
    summary             TEXT,
    confidence_score    NUMERIC(5,4) NOT NULL,
    status              TEXT NOT NULL DEFAULT 'active',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- obligations
CREATE TABLE IF NOT EXISTS obligations (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    norm_id             UUID NOT NULL REFERENCES norms(id) ON DELETE CASCADE,
    obligation_code     TEXT UNIQUE,
    subject_scope       JSONB NOT NULL DEFAULT '{}',
    trigger_conditions  JSONB,
    required_actions    JSONB NOT NULL DEFAULT '[]',
    deadline_rules      JSONB,
    risk_level          TEXT,
    confidence_score    NUMERIC(5,4) NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- obligation_sources
CREATE TABLE IF NOT EXISTS obligation_sources (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    obligation_id       UUID NOT NULL REFERENCES obligations(id) ON DELETE CASCADE,
    fragment_id         UUID NOT NULL REFERENCES document_fragments(id) ON DELETE CASCADE,
    source_role         TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(obligation_id, fragment_id)
);

-- subject_profiles
CREATE TABLE IF NOT EXISTS subject_profiles (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    subject_type        TEXT NOT NULL,
    regulator           TEXT,
    extra_criteria      JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- internal_documents
CREATE TABLE IF NOT EXISTS internal_documents (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    title               TEXT NOT NULL,
    document_type       TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- internal_document_versions
CREATE TABLE IF NOT EXISTS internal_document_versions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    internal_document_id UUID NOT NULL REFERENCES internal_documents(id) ON DELETE CASCADE,
    source_blob_key     TEXT NOT NULL,
    content_hash        TEXT NOT NULL,
    parse_status        TEXT NOT NULL DEFAULT 'pending',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(internal_document_id, content_hash)
);

-- doc_check_jobs
CREATE TABLE IF NOT EXISTS doc_check_jobs (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    internal_document_id UUID REFERENCES internal_documents(id) ON DELETE CASCADE,
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    status              TEXT NOT NULL DEFAULT 'queued',
    progress            INTEGER NOT NULL DEFAULT 0,
    result_json         JSONB,
    error_message       TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- doc_check_findings
CREATE TABLE IF NOT EXISTS doc_check_findings (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id              UUID NOT NULL REFERENCES doc_check_jobs(id) ON DELETE CASCADE,
    obligation_id       UUID REFERENCES obligations(id),
    finding_type        TEXT NOT NULL,
    summary             TEXT NOT NULL,
    details             JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- answer_sessions
CREATE TABLE IF NOT EXISTS answer_sessions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    channel             TEXT NOT NULL,
    question_text       TEXT NOT NULL,
    profile_snapshot    JSONB,
    status              TEXT NOT NULL DEFAULT 'pending',
    refusal_reason      TEXT,
    final_answer_json   JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- answer_evidence
CREATE TABLE IF NOT EXISTS answer_evidence (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    answer_session_id   UUID NOT NULL REFERENCES answer_sessions(id) ON DELETE CASCADE,
    fragment_id         UUID NOT NULL REFERENCES document_fragments(id),
    obligation_id       UUID NULL REFERENCES obligations(id),
    prompt_hash         TEXT,
    verifier_model      TEXT,
    verifier_result     JSONB,
    rules_result        JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- outbox_events
CREATE TABLE IF NOT EXISTS outbox_events (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type          TEXT NOT NULL,
    aggregate_id        TEXT NOT NULL,
    payload             JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- admin_overrides
CREATE TABLE IF NOT EXISTS admin_overrides (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    override_type       TEXT NOT NULL,
    target_id           UUID NOT NULL,
    reason              TEXT NOT NULL,
    created_by          UUID NOT NULL REFERENCES users(id),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- indexes
CREATE INDEX IF NOT EXISTS idx_documents_regulator_code ON documents(regulator_code);
CREATE INDEX IF NOT EXISTS idx_document_versions_document_id_current ON document_versions(document_id, is_current);
CREATE INDEX IF NOT EXISTS idx_fragments_version_id ON document_fragments(document_version_id);
CREATE INDEX IF NOT EXISTS idx_norms_status ON norms(status);
CREATE INDEX IF NOT EXISTS idx_obligations_norm_id ON obligations(norm_id);
CREATE INDEX IF NOT EXISTS idx_internal_documents_tenant_id ON internal_documents(tenant_id);
CREATE INDEX IF NOT EXISTS idx_answer_sessions_tenant_created ON answer_sessions(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_answer_evidence_answer_session ON answer_evidence(answer_session_id);
CREATE INDEX IF NOT EXISTS idx_obligations_subject_scope_gin ON obligations USING GIN(subject_scope);
CREATE INDEX IF NOT EXISTS idx_obligations_required_actions_gin ON obligations USING GIN(required_actions);
CREATE INDEX IF NOT EXISTS idx_usage_ledger_tenant ON usage_ledger(tenant_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_outbox_events_created ON outbox_events(created_at);

-- seed data: demo tenant + admin user
INSERT INTO tenants (id, code, display_name, status) VALUES
    ('00000000-0000-0000-0000-000000000001', 'demo', 'Demo Tenant', 'active')
ON CONFLICT (code) DO NOTHING;

INSERT INTO users (id, tenant_id, email, password_hash, role) VALUES
    ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'admin@podft.ru',
     '$2b$12$LJ3m4ys3Lk0TSwHnbfOMiOXPm1Q5q9Gz0q0q0q0q0q0q0q0q0q', 'admin')
ON CONFLICT (email) DO NOTHING;

INSERT INTO subscriptions (id, tenant_id, tier, monthly_quota) VALUES
    ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'free', 100)
ON CONFLICT (id) DO NOTHING;

-- seed data: Tier-1 source domains
INSERT INTO source_domains (id, domain, source_type, regulator_name, tier) VALUES
    ('00000000-0000-0000-0000-000000000010', 'fedsfm.ru', 'government', 'Росфинмониторинг', 1),
    ('00000000-0000-0000-0000-000000000011', 'cbr.ru', 'government', 'Банк России', 1),
    ('00000000-0000-0000-0000-000000000012', 'publication.pravo.gov.ru', 'government', 'Официальное опубликование', 1)
ON CONFLICT (domain) DO NOTHING;
