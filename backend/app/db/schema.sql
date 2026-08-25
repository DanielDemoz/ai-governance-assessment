-- AI Governance Readiness Assessment — Database Schema
-- SQLite (development) / PostgreSQL (production)
-- Generated from SQLAlchemy models; see backend/app/models/

-- =============================================================================
-- REFERENCE DATA: Categories (nine governance dimensions)
-- =============================================================================

CREATE TABLE IF NOT EXISTS categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    code            VARCHAR(64) NOT NULL UNIQUE,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    weight          NUMERIC(5, 2) NOT NULL,  -- percentage, e.g. 15.00
    sort_order      INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- REFERENCE DATA: Questions (seeded per category)
-- =============================================================================

CREATE TABLE IF NOT EXISTS questions (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id             INTEGER NOT NULL REFERENCES categories(id),
    code                    VARCHAR(64) NOT NULL UNIQUE,
    text                    TEXT NOT NULL,
    governance_objective    TEXT,
    risk_level              VARCHAR(32) NOT NULL DEFAULT 'medium',
    sort_order              INTEGER NOT NULL DEFAULT 0,
    recommendation_key      VARCHAR(128),
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category_id);

-- =============================================================================
-- ASSESSMENT SESSION
-- =============================================================================

CREATE TABLE IF NOT EXISTS assessments (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    public_id       VARCHAR(36) NOT NULL UNIQUE,
    status          VARCHAR(32) NOT NULL DEFAULT 'draft',
    is_demo         BOOLEAN NOT NULL DEFAULT 0,
    completed_at    TIMESTAMP,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_assessments_public_id ON assessments(public_id);

-- =============================================================================
-- ORGANIZATION PROFILE
-- =============================================================================

CREATE TABLE IF NOT EXISTS organizations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id       INTEGER NOT NULL UNIQUE REFERENCES assessments(id) ON DELETE CASCADE,
    name                VARCHAR(255) NOT NULL,
    organization_type   VARCHAR(32) NOT NULL,
    industry            VARCHAR(255),
    country             VARCHAR(128),
    assessment_owner    VARCHAR(255),
    assessment_date     DATE,
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- AI SYSTEM PROFILE
-- =============================================================================

CREATE TABLE IF NOT EXISTS ai_systems (
    id                              INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id                   INTEGER NOT NULL UNIQUE REFERENCES assessments(id) ON DELETE CASCADE,
    name                            VARCHAR(255) NOT NULL,
    description                     TEXT,
    primary_purpose                 TEXT,
    technology_type                 VARCHAR(32),
    vendor_type                     VARCHAR(32),
    development_status              VARCHAR(32),
    deployment_status               VARCHAR(32),
    processes_personal_info         BOOLEAN NOT NULL DEFAULT 0,
    processes_sensitive_info        BOOLEAN NOT NULL DEFAULT 0,
    processes_public_data           BOOLEAN NOT NULL DEFAULT 0,
    processes_employee_data         BOOLEAN NOT NULL DEFAULT 0,
    processes_customer_data         BOOLEAN NOT NULL DEFAULT 0,
    processes_student_data          BOOLEAN NOT NULL DEFAULT 0,
    processes_health_info           BOOLEAN NOT NULL DEFAULT 0,
    processes_financial_info        BOOLEAN NOT NULL DEFAULT 0,
    makes_decisions_about_people    BOOLEAN NOT NULL DEFAULT 0,
    recommends_decisions            BOOLEAN NOT NULL DEFAULT 0,
    can_materially_affect_individual BOOLEAN NOT NULL DEFAULT 0,
    affects_employment              BOOLEAN NOT NULL DEFAULT 0,
    affects_education               BOOLEAN NOT NULL DEFAULT 0,
    affects_healthcare              BOOLEAN NOT NULL DEFAULT 0,
    affects_financial_access        BOOLEAN NOT NULL DEFAULT 0,
    affects_public_services         BOOLEAN NOT NULL DEFAULT 0,
    affects_housing                 BOOLEAN NOT NULL DEFAULT 0,
    affects_insurance               BOOLEAN NOT NULL DEFAULT 0,
    affects_legal_rights            BOOLEAN NOT NULL DEFAULT 0,
    created_at                      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at                      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- QUESTIONNAIRE RESPONSES
-- Response values: 0–4 (scored), -1 (not applicable, excluded from denominator)
-- =============================================================================

CREATE TABLE IF NOT EXISTS responses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id   INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    question_id     INTEGER NOT NULL REFERENCES questions(id),
    response_value  INTEGER NOT NULL,
    notes           TEXT,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (assessment_id, question_id)
);

CREATE INDEX IF NOT EXISTS idx_responses_assessment ON responses(assessment_id);

-- =============================================================================
-- GOVERNANCE RISK MATRIX ENTRIES
-- Risk Score = likelihood (1–5) × impact (1–5)
-- =============================================================================

CREATE TABLE IF NOT EXISTS risks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id   INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    risk_type       VARCHAR(64) NOT NULL,
    description     TEXT,
    likelihood      INTEGER NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
    impact          INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
    risk_score      INTEGER NOT NULL,
    classification  VARCHAR(32) NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_risks_assessment ON risks(assessment_id);

-- =============================================================================
-- RULE-BASED RECOMMENDATIONS
-- =============================================================================

CREATE TABLE IF NOT EXISTS recommendations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id       INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    category_id         INTEGER REFERENCES categories(id),
    question_id         INTEGER REFERENCES questions(id),
    priority            VARCHAR(32) NOT NULL,
    identified_gap      TEXT NOT NULL,
    recommendation      TEXT NOT NULL,
    why_it_matters      TEXT NOT NULL,
    suggested_action    TEXT NOT NULL,
    responsible_role    VARCHAR(255) NOT NULL,
    suggested_timeframe VARCHAR(128) NOT NULL,
    source_rule_key     VARCHAR(128),
    created_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_recommendations_assessment ON recommendations(assessment_id);

-- =============================================================================
-- COMPUTED ASSESSMENT RESULTS (deterministic — never LLM-generated)
-- =============================================================================

CREATE TABLE IF NOT EXISTS assessment_results (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id           INTEGER NOT NULL UNIQUE REFERENCES assessments(id) ON DELETE CASCADE,
    overall_score           REAL NOT NULL,
    readiness_level         VARCHAR(32) NOT NULL,
    ai_system_risk          VARCHAR(32) NOT NULL,
    governance_gap          VARCHAR(32) NOT NULL,
    category_scores_json    TEXT NOT NULL,
    calculation_trace_json  TEXT,
    calculated_at           TIMESTAMP NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- GENERATED REPORTS
-- =============================================================================

CREATE TABLE IF NOT EXISTS reports (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id   INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    format          VARCHAR(16) NOT NULL DEFAULT 'pdf',
    file_path       VARCHAR(512),
    generated_at    TIMESTAMP NOT NULL,
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reports_assessment ON reports(assessment_id);

-- =============================================================================
-- SEED DATA: Categories (weights total 100%)
-- =============================================================================

INSERT OR IGNORE INTO categories (code, name, weight, sort_order, description) VALUES
    ('accountability', 'Accountability & Governance', 15.00, 1,
     'Governance structure, ownership, policies, and oversight'),
    ('human_oversight', 'Human Oversight', 15.00, 2,
     'Human involvement, override capability, and decision review'),
    ('privacy', 'Privacy & Data Governance', 15.00, 3,
     'Data collection, retention, access controls, and privacy risks'),
    ('fairness', 'Fairness & Non-Discrimination', 15.00, 4,
     'Bias testing, demographic analysis, and fairness monitoring'),
    ('transparency', 'Transparency & Explainability', 10.00, 5,
     'AI disclosure, documentation, and explainability'),
    ('security', 'Security & Robustness', 10.00, 6,
     'Cybersecurity, input validation, and incident response'),
    ('risk_management', 'AI Impact & Risk Management', 10.00, 7,
     'Impact assessment, harm documentation, and approval processes'),
    ('lifecycle', 'Monitoring & Lifecycle Management', 5.00, 8,
     'Post-deployment monitoring, drift detection, and retirement'),
    ('affected_people', 'Accountability to Affected People', 5.00, 9,
     'Complaints process, challenge rights, and remediation');
