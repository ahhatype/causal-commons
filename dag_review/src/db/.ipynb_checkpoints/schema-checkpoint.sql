CREATE TABLE studies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    authors TEXT,
    doi TEXT,
    source TEXT,
    year INT,
    llm_model_used TEXT,
    date_processed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE objectives (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    content TEXT,
    type TEXT,
    confidence_score FLOAT,
    validated BOOLEAN DEFAULT FALSE
);

CREATE TABLE eligibility_criteria (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    criteria TEXT,
    inclusion BOOLEAN,
    validated BOOLEAN DEFAULT FALSE
);

CREATE TABLE outcomes (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    data JSONB,
    validated BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_outcomes_data ON outcomes USING GIN (data);

CREATE TABLE exposures (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    exposure TEXT,
    validated BOOLEAN DEFAULT FALSE
);

CREATE TABLE confounders (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    term TEXT,
    source TEXT,
    confidence FLOAT,
    validated BOOLEAN DEFAULT FALSE,
    notes TEXT
);

CREATE TABLE comorbidities (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    condition TEXT,
    source TEXT,
    validated BOOLEAN DEFAULT FALSE
);

CREATE TABLE dag_nodes (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    node_label TEXT,
    node_type TEXT,
    source TEXT
);

CREATE TABLE dag_edges (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    from_node_id INT REFERENCES dag_nodes(id),
    to_node_id INT REFERENCES dag_nodes(id),
    relation_type TEXT,
    confidence FLOAT
);

CREATE TABLE validation_status (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    human_reviewed BOOLEAN DEFAULT FALSE,
    discrepancy_score FLOAT,
    match_method TEXT,
    overlap_terms TEXT[],
    notes TEXT
);

CREATE TABLE extraction_reviews (
    id SERIAL PRIMARY KEY,
    study_id INT REFERENCES studies(id),
    raw_llm_json JSONB NOT NULL,
    user_json JSONB NOT NULL,
    user_edited BOOLEAN DEFAULT FALSE,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


