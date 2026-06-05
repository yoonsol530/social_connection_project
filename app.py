import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="분석1: 음주율과 단체참여율",
    layout="wide"
)

st.title("분석1: 음주율 감소와 단체참여 감소는 함께 나타났는가?")

st.markdown("""
이 페이지는 국민건강영양조사의 **소득수준별 월간음주율**과  
국민여가활동조사의 **소득수준별 단체참여율**을 결합하여 분석한 결과입니다.

두 데이터는 **연도(year)** 와 **소득집단(income_group)** 을 기준으로 SQL JOIN 하였습니다.
""")

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

income_order = ["하", "중하", "중", "중상", "상"]

df["income_group"] = pd.Categorical(
    df["income_group"],
    categories=income_order,
    ordered=True
)

df = df.sort_values(["year", "income_group"])

st.header("1. SQL JOIN 결과")
st.code(query, language="sql")
st.dataframe(df, use_container_width=True)

st.header("2. 소득수준별 월간음주율 추이")

fig1 = px.line(
    df,
    x="year",
    y="drinking_rate",
    color="income_group",
    markers=True,
    labels={
        "year": "연도",
        "drinking_rate": "월간음주율(%)",
        "income_group": "소득집단"
    },
    title="소득수준별 월간음주율 변화"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
**해석:** 2019년 대비 2023년에 모든 소득집단에서 월간음주율이 감소했습니다.  
특히 저소득층(하)의 감소폭이 가장 크게 나타났습니다.
""")

st.header("3. 소득수준별 단체참여율 추이")

fig2 = px.line(
    df,
    x="year",
    y="participation_rate",
    color="income_group",
    markers=True,
    labels={
        "year": "연도",
        "participation_rate": "단체참여율(%)",
        "income_group": "소득집단"
    },
    title="소득수준별 단체참여율 변화"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
**해석:** 단체참여율 역시 2019년 대비 2023년에 모든 소득집단에서 감소했습니다.  
또한 모든 시점에서 소득수준이 높을수록 단체참여율이 높게 나타나는 경향이 유지되었습니다.
""")

st.header("4. 2019→2023 감소폭 비교")

df_2019 = df[df["year"] == 2019]
df_2023 = df[df["year"] == 2023]

change = pd.merge(
    df_2019,
    df_2023,
    on="income_group",
    suffixes=("_2019", "_2023")
)

change["drinking_drop"] = (
    change["drinking_rate_2019"] - change["drinking_rate_2023"]
)

change["participation_drop"] = (
    change["participation_rate_2019"] - change["participation_rate_2023"]
)

change_table = change[
    ["income_group", "drinking_drop", "participation_drop"]
]

st.dataframe(change_table, use_container_width=True)

fig3 = px.scatter(
    change_table,
    x="drinking_drop",
    y="participation_drop",
    text="income_group",
    labels={
        "drinking_drop": "음주율 감소폭(%p)",
        "participation_drop": "단체참여율 감소폭(%p)",
        "income_group": "소득집단"
    },
    title="소득집단별 음주율 감소폭과 단체참여율 감소폭"
)

fig3.update_traces(
    textposition="top center",
    marker=dict(size=12)
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
**핵심 인사이트:** 저소득층(하)은 음주율 감소폭 **6.0%p**,  
단체참여율 감소폭 **약 6.97%p**로 두 지표 모두에서 가장 큰 감소폭을 보였습니다.

이는 동일 소득집단 안에서 음주율 감소와 단체참여율 감소가 함께 나타났음을 보여줍니다.

다만 이 분석은 집계자료 기반이므로,  
개인 수준에서 “음주 감소가 단체참여 감소를 직접 초래했다”고 해석할 수는 없습니다.
""")

st.header("5. 분석1 요약")

st.success("""
국민건강영양조사와 국민여가활동조사를 연도와 소득집단 기준으로 결합한 결과,
2019년 대비 2023년에 모든 소득집단에서 월간음주율과 단체참여율이 감소했습니다.

특히 저소득층에서 두 지표의 감소폭이 가장 크게 나타났습니다.

이는 코로나 이후 사회적 교류와 관련된 활동이 소득집단별로 다르게 변화했을 가능성을 시사합니다.

단, 본 분석은 집계자료 기반 분석이므로 인과관계가 아니라
동일 소득집단 내 동반 변화 패턴을 확인한 결과입니다.
""")

conn.close()