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
"""

df = pd.read_sql_query(query, conn)

df2019 = df[df["year"] == 2019]
df2023 = df[df["year"] == 2023]

merged = pd.merge(
    df2019,
    df2023,
    on="income_group",
    suffixes=("_2019", "_2023")
)

merged["drinking_drop"] = (
    merged["drinking_rate_2019"]
    - merged["drinking_rate_2023"]
)

merged["participation_drop"] = (
    merged["participation_rate_2019"]
    - merged["participation_rate_2023"]
)

print(
    merged[
        [
            "income_group",
            "drinking_drop",
            "participation_drop"
        ]
    ]
)

conn.close()