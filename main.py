from snowflake.snowpark import Session
from dotenv import load_dotenv
import os
import snowflake_setup
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# .env 파일 로드
load_dotenv(dotenv_path=".env")

# 세션 연결 설정
connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

session = Session.builder.configs(connection_parameters).create()

# 처음 한 번만 실행
# snowflake_setup.initialize_snowflake_environment(session)

df = session.table("personality_survey")
df_pd = df.to_pandas()

behavior_cols = [
    "TIME_SPENT_ALONE",
    "GOING_OUTSIDE",
    "FRIENDS_CIRCLE_SIZE",
    "POST_FREQUENCY",
    "SOCIAL_EVENT_ATTENDANCE"
]

mean_df = df_pd.groupby("PERSONALITY")[behavior_cols].mean().reset_index()

st.title("성격 유형별 평균 생활 패턴 비교")
for col in behavior_cols:
    fig = px.bar(
        mean_df,
        x = "PERSONALITY",
        y = col,
        title = f"{col} 평균 비교",
        labels = {"PERSONALITY": "성격", col: "평균값"}
    )
    st.plotly_chart(fig)


    