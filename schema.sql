-- FarmDesk Supabase Schema

-- Plots Table
CREATE TABLE plots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Plants Table
-- A teak farm with 3500 teak trees and 9000 black pepper vines across 30 plots
-- Each plot has 15 rows x 20 columns x 3 vines A/B/C
CREATE TABLE plants (
    id VARCHAR(50) PRIMARY KEY, -- e.g., P1-R1-C1-A
    plot_id INTEGER REFERENCES plots(id) ON DELETE CASCADE,
    row_num INTEGER NOT NULL,
    col_num INTEGER NOT NULL,
    vine_type VARCHAR(1) NOT NULL, -- A, B, or C
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Survey Entries Table
CREATE TABLE survey_entries (
    id SERIAL PRIMARY KEY,
    plant_id VARCHAR(50) REFERENCES plants(id) ON DELETE CASCADE,
    height_ft INTEGER,
    height_in INTEGER,
    fertilizer_qty NUMERIC, -- in kg
    fertilizer_type VARCHAR(255),
    disease_tags TEXT[], -- array of tags
    notes TEXT,
    survey_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
