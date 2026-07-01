// pod-ft Neo4j constraints
// schema-ref: project-schema.yaml#/databases/neo4j
// Applied during Neo4j initialization (Sprint 3+)

CREATE CONSTRAINT regulator_id IF NOT EXISTS FOR (n:Regulator) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT document_id IF NOT EXISTS FOR (n:Document) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT document_version_id IF NOT EXISTS FOR (n:DocumentVersion) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT fragment_id IF NOT EXISTS FOR (n:Fragment) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT norm_id IF NOT EXISTS FOR (n:Norm) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT obligation_id IF NOT EXISTS FOR (n:Obligation) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT subject_type_code IF NOT EXISTS FOR (n:SubjectType) REQUIRE n.code IS UNIQUE;
CREATE CONSTRAINT criterion_code IF NOT EXISTS FOR (n:ApplicabilityCriterion) REQUIRE n.code IS UNIQUE;
