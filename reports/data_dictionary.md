\# Bluestock Mutual Fund Analytics - Data Dictionary



\## 01\_fund\_master



| Column | Type | Description |

|----------|--------|------------|

| amfi\_code | INTEGER | Unique mutual fund identifier |

| scheme\_name | TEXT | Scheme name |

| fund\_house | TEXT | Asset management company |

| category | TEXT | Fund category |

| sub\_category | TEXT | Fund sub-category |

| risk\_category | TEXT | Risk classification |



\---



\## 02\_nav\_history



| Column | Type | Description |

|----------|--------|------------|

| amfi\_code | INTEGER | Fund identifier |

| date | DATE | NAV date |

| nav | REAL | Net Asset Value |



\---



\## 03\_aum\_by\_fund\_house



| Column | Type | Description |

|----------|--------|------------|

| fund\_house | TEXT | Asset management company |

| aum\_crore | REAL | Assets under management |



\---



\## 04\_monthly\_sip\_inflows



| Column | Type | Description |

|----------|--------|------------|

| month | TEXT | Reporting month |

| sip\_inflow\_crore | REAL | SIP inflow amount |



\---



\## 05\_category\_inflows



| Column | Type | Description |

|----------|--------|------------|

| category | TEXT | Mutual fund category |

| net\_inflow\_crore | REAL | Net inflow |



\---



\## 06\_industry\_folio\_count



| Column | Type | Description |

|----------|--------|------------|

| month | TEXT | Reporting month |

| total\_folios\_crore | REAL | Total folios |



\---



\## 07\_scheme\_performance



| Column | Type | Description |

|----------|--------|------------|

| return\_1yr\_pct | REAL | 1-year return |

| return\_3yr\_pct | REAL | 3-year return |

| return\_5yr\_pct | REAL | 5-year return |

| expense\_ratio\_pct | REAL | Expense ratio |



\---



\## 08\_investor\_transactions



| Column | Type | Description |

|----------|--------|------------|

| transaction\_type | TEXT | SIP/Lumpsum/Redemption |

| amount\_inr | REAL | Transaction amount |

| transaction\_date | DATE | Transaction date |



\---



\## 09\_portfolio\_holdings



| Column | Type | Description |

|----------|--------|------------|

| company\_name | TEXT | Security held |

| sector | TEXT | Sector classification |

| market\_value\_cr | REAL | Market value |



\---



\## 10\_benchmark\_indices



| Column | Type | Description |

|----------|--------|------------|

| date | DATE | Index date |

| close | REAL | Closing value |

