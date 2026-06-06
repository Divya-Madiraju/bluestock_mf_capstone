-- =============================================
-- BLUESTOCK MF CAPSTONE — 10 ANALYTICAL QUERIES
-- =============================================

-- Q1: Top 5 funds by AUM
SELECT
    f.fund_name,
    f.fund_house,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- Q2: Average NAV per month (all funds)
SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Q3: SIP transaction count year-over-year growth
SELECT
    d.year,
    COUNT(*) AS sip_count,
    SUM(t.amount) AS total_sip_amount
FROM fact_transactions t
JOIN dim_date d ON t.date = d.date
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;

-- Q4: Total transactions by investor state
SELECT
    investor_state,
    COUNT(*) AS txn_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions
GROUP BY investor_state
ORDER BY total_amount DESC;

-- Q5: Funds with expense ratio less than 1%
SELECT
    f.fund_name,
    f.fund_house,
    f.category,
    p.expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- Q6: Best performing funds by 1-year returns
SELECT
    f.fund_name,
    f.category,
    p.returns_1y,
    p.returns_3y,
    p.returns_5y
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.returns_1y IS NOT NULL
ORDER BY p.returns_1y DESC
LIMIT 10;

-- Q7: Funds with highest Sharpe ratio (risk-adjusted return)
SELECT
    f.fund_name,
    f.category,
    p.sharpe_ratio,
    p.returns_1y
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.sharpe_ratio IS NOT NULL
ORDER BY p.sharpe_ratio DESC
LIMIT 10;

-- Q8: Transaction breakdown by type and KYC status
SELECT
    transaction_type,
    kyc_status,
    COUNT(*) AS txn_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type, kyc_status
ORDER BY transaction_type, total_amount DESC;

-- Q9: Month with highest NAV for each fund (peak NAV date)
SELECT
    f.fund_name,
    n.date,
    n.nav AS peak_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
WHERE n.nav = (
    SELECT MAX(nav)
    FROM fact_nav
    WHERE amfi_code = n.amfi_code
)
ORDER BY peak_nav DESC;

-- Q10: Category-wise average returns and expense ratio
SELECT
    f.category,
    COUNT(DISTINCT f.amfi_code) AS fund_count,
    ROUND(AVG(p.returns_1y), 2) AS avg_return_1y,
    ROUND(AVG(p.returns_3y), 2) AS avg_return_3y,
    ROUND(AVG(p.expense_ratio), 2) AS avg_expense_ratio
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY avg_return_1y DESC;