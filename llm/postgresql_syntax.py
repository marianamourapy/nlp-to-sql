POSTGRESQL_SYNTAX = """
POSTGRESQL SYNTAX REFERENCE:

DATE FUNCTIONS:
- Never use STRFTIME() — use EXTRACT() or TO_CHAR() instead
- Filter by month: EXTRACT(MONTH FROM column) = 2
- Filter by year: EXTRACT(YEAR FROM column) = 2024

GROUP BY:
- Every non-aggregated column in SELECT must appear in GROUP BY

STRING MATCHING:
- Always use ILIKE instead of = for text comparisons
- ILIKE is case-insensitive: 'Macbook', 'MacBook', 'MACBOOK' all match

NEGATIVE CONDITIONS:
- For exclusion queries use NOT IN with a subquery
- In NOT IN subqueries, always use ILIKE for text comparisons

AGGREGATIONS:
- Always include the aggregated value in SELECT alongside the name
"""