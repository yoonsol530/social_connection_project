import sqlite3
import pandas as pd

drinking = pd.read_csv("drinking_rate.csv")
participation = pd.read_csv("group_participation.csv")

conn = sqlite3.connect("social_connection.db")

drinking.to_sql("drinking_rate", conn, if_exists="replace", index=False)
participation.to_sql("group_participation", conn, if_exists="replace", index=False)

conn.close()

print("DB 생성 완료")