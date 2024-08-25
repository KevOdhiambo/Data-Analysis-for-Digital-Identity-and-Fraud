-- Fraud rate by verification method
SELECT 
    verification_method,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN fraud_flag = 1 THEN 1 ELSE 0 END) as fraud_count,
    ROUND(CAST(SUM(CASE WHEN fraud_flag = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as fraud_rate
FROM 
    transactions
GROUP BY 
    verification_method
ORDER BY 
    fraud_rate DESC;

-- Verification success rate by country
SELECT 
    country,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN verification_success = 1 THEN 1 ELSE 0 END) as successful_verifications,
    ROUND(CAST(SUM(CASE WHEN verification_success = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as success_rate
FROM 
    transactions
GROUP BY 
    country
ORDER BY 
    success_rate DESC;

-- Average transaction amount by device type and fraud flag
SELECT 
    device_type,
    fraud_flag,
    ROUND(AVG(transaction_amount), 2) as avg_transaction_amount
FROM 
    transactions
GROUP BY 
    device_type,
    fraud_flag
ORDER BY 
    device_type,
    fraud_flag;