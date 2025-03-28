CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    company_name VARCHAR(255),
    industry VARCHAR(255),
    market_cap BIGINT,
    currency VARCHAR(10),
    current_price NUMERIC,
    per NUMERIC,
    roe NUMERIC,
    roa NUMERIC,
    fcf BIGINT,
    total_revenue BIGINT,
    net_income BIGINT,
    gross_margin NUMERIC,
    operating_margin NUMERIC,
    net_margin NUMERIC,
    dividend_yield NUMERIC,
    total_debt BIGINT,
    total_equity BIGINT,
    cash BIGINT,
    total_assets BIGINT,
    current_liabilities BIGINT,
    shares_outstanding BIGINT,
    revenue_per_share NUMERIC,
    earnings_per_share NUMERIC,
    fcf_per_share NUMERIC,
    fcf_yield NUMERIC,
    price_to_fcf NUMERIC,
    freecashflow_margin NUMERIC,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);