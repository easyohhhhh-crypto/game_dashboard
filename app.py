import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------------------------------
# 페이지 설정
# -------------------------------------------------
st.set_page_config(
    page_title="영상물 등급 분류 대시보드",
    layout="wide"
)

st.title("영상물 등급 분류 대시보드")

# -------------------------------------------------
# 데이터 불러오기
# -------------------------------------------------
df = pd.read_excel("game_data.xls")

# -------------------------------------------------
# 컬럼명 정리
# -------------------------------------------------
df.columns = [str(col).strip() for col in df.columns]

# -------------------------------------------------
# 데이터 미리보기
# -------------------------------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# -------------------------------------------------
# 컬럼 자동 탐색
# -------------------------------------------------
rating_col = None
genre_col = None
year_col = None
company_col = None

for col in df.columns:

    col_lower = str(col).lower()

    # 등급
    if rating_col is None and (
        "등급" in str(col) or
        "rating" in col_lower or
        "분류" in str(col)
    ):
        rating_col = col

    # 장르
    if genre_col is None and (
        "장르" in str(col) or
        "genre" in col_lower
    ):
        genre_col = col

    # 연도
    if year_col is None and (
        "연도" in str(col) or
        "년도" in str(col) or
        "year" in col_lower
    ):
        year_col = col

    # 회사
    if company_col is None and (
        "회사" in str(col) or
        "업체" in str(col) or
        "publisher" in col_lower or
        "제작" in str(col)
    ):
        company_col = col

# -------------------------------------------------
# 사이드바 필터
# -------------------------------------------------
st.sidebar.header("필터")

if rating_col:

    rating_options = df[rating_col].dropna().unique()

    selected_rating = st.sidebar.multiselect(
        "등급 선택",
        rating_options,
        default=rating_options
    )

    df = df[df[rating_col].isin(selected_rating)]

# -------------------------------------------------
# 등급 분포 그래프
# -------------------------------------------------
if rating_col:

    st.header("📊 영상물 등급 분포")

    rating_count = (
        df[rating_col]
        .value_counts()
        .reset_index()
    )

    rating_count.columns = ["등급", "영상수"]

    fig = px.bar(
        rating_count,
        x="등급",
        y="영상수",
        text="영상수"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -------------------------------------------------
# 연도별 변화
# -------------------------------------------------
if rating_col and year_col:

    st.header("📈 연도별 영상 등급 변화")

    year_rating = (
        df.groupby([year_col, rating_col])
        .size()
        .reset_index(name="count")
    )

    fig2 = px.line(
        year_rating,
        x=year_col,
        y="count",
        color=rating_col
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -------------------------------------------------
# 장르별 히트맵
# -------------------------------------------------
if rating_col and genre_col:

    st.header("🔥 장르별 영상 등급 히트맵")

    heatmap_data = pd.crosstab(
        df[genre_col],
        df[rating_col]
    )

    fig3, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt="d",
        cmap="YlOrRd",
        ax=ax
    )

    st.pyplot(fig3)

# -------------------------------------------------
# 회사별 TOP 10
# -------------------------------------------------
if company_col:

    st.header("🏢 회사별 영상 비율 TOP 10")

    top_company = (
        df[company_col]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_company.columns = ["회사", "영상수"]

    fig4 = px.pie(
        top_company,
        names="회사",
        values="게임수"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )
