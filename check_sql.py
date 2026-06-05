import sqlite3
import pandas as pd

conn = sqlite3.connect("social_connection.db")

query = """
SELECT
    d.year,
    d.income_group,
    d.drinking_rate,
    g.participation_rate
FROM drinking_rate d
JOIN group_participation g
ON d.year = g.year
AND d.income_group = g.income_group
ORDER BY d.year, d.income_group;
"""

df = pd.read_sql_query(query, conn)

print(df)

conn.close()