-- Customer Churn & Retention Spend — SQL cohort queries
-- These mirror the in-memory SQLite queries in data_analysis.py

-- 1) Churn by contract type (month-to-month vs 1-year vs 2-year)
SELECT
    Contract AS segment,
    COUNT(*) AS total_customers,
    SUM(ChurnFlag) AS churned_customers,
    ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 2) Churn by tenure band (3–6 month danger zone)
SELECT
    tenure_band AS segment,
    COUNT(*) AS total_customers,
    SUM(ChurnFlag) AS churned_customers,
    ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
FROM customers
GROUP BY tenure_band;

-- 3) Churn by internet service type
SELECT
    InternetService AS segment,
    COUNT(*) AS total_customers,
    SUM(ChurnFlag) AS churned_customers,
    ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
FROM customers
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;

-- 4) Churn by payment method (electronic check vs autopay)
SELECT
    payment_group AS segment,
    COUNT(*) AS total_customers,
    SUM(ChurnFlag) AS churned_customers,
    ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS revenue_at_risk,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge,
    ROUND(SUM(CASE WHEN ChurnFlag = 1 THEN MonthlyCharges * 12 ELSE 0 END), 2) AS annual_revenue_at_risk
FROM customers
GROUP BY payment_group
ORDER BY churn_rate_pct DESC;

-- 5) Cross-cohort heatmap source: contract × tenure
SELECT
    Contract,
    tenure_band,
    COUNT(*) AS total_customers,
    SUM(ChurnFlag) AS churned_customers,
    ROUND(100.0 * SUM(ChurnFlag) * 1.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract, tenure_band;

-- Formulas
-- Churn Rate (%) = (Churned Customers ÷ Total Customers) × 100
-- Revenue at Risk = Σ (Monthly Charges of Churned Customers)
