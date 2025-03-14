CREATE TABLE portfolio (
    ticker VARCHAR(50) PRIMARY KEY,
    quantity INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);