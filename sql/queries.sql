-- Bluestock Mutual Fund Analytics - validation & analytical queries (Day 2)

-- == VALIDATION ==

-- V1: row count per table
SELECT 'fund_master' AS tbl, COUNT(*) AS rows FROM fund_master
UNION ALL SELECT 'nav_history', COUNT(*) FROM nav_history
UNION ALL SELECT 'aum_by_fund_house', COUNT(*) FROM aum_by_fund_house
UNION ALL SELECT 'monthly_sip_inflows', COUNT(*) FROM monthly_sip_inflows
UNION ALL SELECT 'category_inflows', COUNT(*) FROM category_inflows
UNION ALL SELECT 'industry_folio_count', COUNT(*) FROM industry_folio_count
UNION ALL SELECT 'scheme_performance', COUNT(*) FROM scheme_performance
UNION ALL SELECT 'investor_transactions', COUNT(*) FROM investor_transactions
UNION ALL SELECT 'portfolio_holdings', COUNT(*) FROM portfolio_holdings
UNION ALL SELECT 'benchmark_indices', COUNT(*) FROM benchmark_indices;

-- V2: orphan amfi_codes in child tables (expect 0 rows)
SELECT 'nav_history' AS tbl, amfi_code FROM nav_history
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)
UNION SELECT 'scheme_performance', amfi_code FROM scheme_performance
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)
UNION SELECT 'investor_transactions', amfi_code FROM investor_transactions
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master)
UNION SELECT 'portfolio_holdings', amfi_code FROM portfolio_holdings
WHERE amfi_code NOT IN (SELECT amfi_code FROM fund_master);

-- V3: NAV values must be positive (expect 0)
SELECT COUNT(*) AS bad_nav FROM nav_history WHERE nav <= 0;

-- V4: transaction amounts must be positive (expect 0)
SELECT COUNT(*) AS bad_amount FROM investor_transactions WHERE amount_inr <= 0;

-- == ANALYTICS ==

-- A1: scheme count by category / sub_category
SELECT category, sub_category, COUNT(*) AS schemes
FROM fund_master GROUP BY category, sub_category ORDER BY schemes DESC;

-- A2: latest NAV per scheme
SELECT n.amfi_code, f.scheme_name, n.date, n.nav
FROM nav_history n
JOIN fund_master f ON f.amfi_code = n.amfi_code
JOIN (SELECT amfi_code, MAX(date) AS mx FROM nav_history GROUP BY amfi_code) m
  ON m.amfi_code = n.amfi_code AND m.mx = n.date
ORDER BY f.scheme_name;

-- A3: top 10 fund houses by latest AUM
SELECT fund_house, aum_crore, date
FROM aum_by_fund_house
WHERE date = (SELECT MAX(date) FROM aum_by_fund_house)
ORDER BY aum_crore DESC LIMIT 10;

-- A4: top 10 schemes by 3-year return
SELECT amfi_code, scheme_name, return_3yr_pct, sharpe_ratio, risk_grade
FROM scheme_performance ORDER BY return_3yr_pct DESC LIMIT 10;

-- A5: net investment flow by transaction type
SELECT transaction_type,
       COUNT(*) AS txns,
       SUM(amount_inr) AS total_inr
FROM investor_transactions GROUP BY transaction_type ORDER BY total_inr DESC;

-- A6: total SIP inflow by year
SELECT substr(month, 1, 4) AS yr, ROUND(SUM(sip_inflow_crore), 2) AS sip_crore
FROM monthly_sip_inflows GROUP BY yr ORDER BY yr;

-- A7: top sectors by aggregate holding market value
SELECT sector, ROUND(SUM(market_value_cr), 2) AS mkt_value_cr
FROM portfolio_holdings GROUP BY sector ORDER BY mkt_value_cr DESC LIMIT 10;
