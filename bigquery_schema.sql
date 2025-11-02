-- BigQuery schema for LVX startup curation platform
-- Replaces CloudSQL with cost-effective BigQuery tables

-- Applications table
CREATE TABLE `lvx_curation.applications` (
  id STRING NOT NULL,
  company_name STRING,
  submission_time TIMESTAMP,
  status STRING,
  raw_asset_uri STRING,
  applicant_id STRING,
  founders JSON,
  assets JSON,
  source STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Curation metrics definition table
CREATE TABLE `lvx_curation.curation_metrics` (
  id STRING NOT NULL,
  name STRING,
  description STRING,
  category STRING,
  rule_type STRING,
  rule_payload JSON,
  weight_default FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Scoring rules table
CREATE TABLE `lvx_curation.scoring_rules` (
  id STRING NOT NULL,
  category STRING,
  weight_default FLOAT64,
  rule_type STRING,
  rule_payload JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Workflow states table
CREATE TABLE `lvx_curation.workflow_states` (
  run_id STRING NOT NULL,
  app_id STRING,
  status STRING,
  current_step STRING,
  steps_completed JSON,
  retry_count INT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Extraction results table
CREATE TABLE `lvx_curation.extraction_results` (
  id STRING NOT NULL,
  app_id STRING,
  extractor_version STRING,
  extracted_json JSON,
  text_snippets JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Enrichment results table
CREATE TABLE `lvx_curation.enrichment_results` (
  id STRING NOT NULL,
  app_id STRING,
  source STRING,
  url STRING,
  snippet STRING,
  confidence FLOAT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Mapping results table
CREATE TABLE `lvx_curation.mapping_results` (
  id STRING NOT NULL,
  app_id STRING,
  canonical_json JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Score runs table
CREATE TABLE `lvx_curation.score_runs` (
  id STRING NOT NULL,
  app_id STRING,
  scores_json JSON,
  overall_score FLOAT64,
  investor_weights_json JSON,
  decision STRING,
  evidence_refs JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Investment memos table
CREATE TABLE `lvx_curation.investment_memos` (
  id STRING NOT NULL,
  app_id STRING,
  executive_summary STRING,
  sections JSON,
  final_recommendation STRING,
  memo_text STRING,
  memo_pdf_uri STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Voice interview results table
CREATE TABLE `lvx_curation.voice_interviews` (
  id STRING NOT NULL,
  app_id STRING,
  transcript STRING,
  extracted_fields JSON,
  call_duration INT64,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Audit logs table
CREATE TABLE `lvx_curation.audit_logs` (
  id STRING NOT NULL,
  app_id STRING,
  event_type STRING,
  actor STRING,
  details JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert sample curation metrics
INSERT INTO `lvx_curation.curation_metrics` (id, name, category, weight_default) VALUES
('founder_001', 'founder_market_fit_score', 'founder_profile', 0.3),
('founder_002', 'founder_experience_years', 'founder_profile', 0.2),
('market_001', 'total_addressable_market', 'problem_market', 0.25),
('market_002', 'market_growth_rate', 'problem_market', 0.2),
('diff_001', 'technology_novelty_score', 'differentiator', 0.2),
('diff_002', 'ip_portfolio_strength', 'differentiator', 0.15),
('traction_001', 'annual_recurring_revenue', 'team_traction', 0.25),
('traction_002', 'customer_retention_rate', 'team_traction', 0.15);

-- Insert sample scoring rules
INSERT INTO `lvx_curation.scoring_rules` (id, category, weight_default, rule_type) VALUES
('rule_001', 'founder_profile', 0.25, 'weighted_average'),
('rule_002', 'problem_market', 0.25, 'weighted_average'),
('rule_003', 'differentiator', 0.25, 'weighted_average'),
('rule_004', 'team_traction', 0.25, 'weighted_average');