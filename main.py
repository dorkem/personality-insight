from snowflake.snowpark import Session
from dotenv import load_dotenv
import os
import snowflake_setup
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Snowflake 연결
load_dotenv(dotenv_path=".env")

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

# Snowflake 테이블 불러오기
df = session.table("personality_survey")
df_pd = df.to_pandas()

# 2. 데이터 전처리: 문자형 이진 컬럼을 숫자로 변환
df_pd["STAGE_FEAR"] = df_pd["STAGE_FEAR"].map({"Yes": 1, "No": 0})
df_pd["DRAINED_AFTER_SOCIALIZING"] = df_pd["DRAINED_AFTER_SOCIALIZING"].map({"Yes": 1, "No": 0})
df_pd["PERSONALITY"] = df_pd["PERSONALITY"].map({"Extrovert": 1, "Introvert": 0})

# 3. 데이터 나누기
y = df_pd["PERSONALITY"]
X = df_pd.drop("PERSONALITY", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 모델 훈련
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5. 예측 및 평가
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Introvert", "Extrovert"])

# 6. 중요 변수 보기
feature_importance = pd.Series(model.feature_importances_, index=X.columns)
feature_importance = feature_importance.sort_values(ascending=False)

# 7. Streamlit 시각화
st.title("🧠 성격 유형 분석 및 예측")

st.subheader("1️⃣ 성격 유형별 평균 생활 패턴")
behavior_cols = [
    "TIME_SPENT_ALONE",
    "GOING_OUTSIDE",
    "FRIENDS_CIRCLE_SIZE",
    "POST_FREQUENCY",
    "SOCIAL_EVENT_ATTENDANCE"
]
mean_df = df_pd.copy()
mean_df["PERSONALITY"] = mean_df["PERSONALITY"].map({1: "Extrovert", 0: "Introvert"})
mean_df = mean_df.groupby("PERSONALITY")[behavior_cols].mean().reset_index()

for col in behavior_cols:
    fig = px.bar(
        mean_df,
        x="PERSONALITY",
        y=col,
        title=f"{col} 평균 비교",
        labels={"PERSONALITY": "성격", col: "평균값"},
        color="PERSONALITY"
    )
    st.plotly_chart(fig)

st.subheader("2️⃣ RandomForest 모델 성능")
st.write(f"🔍 정확도: **{accuracy:.2f}**")
st.text("📋 분류 리포트:")
st.code(report, language="text")

st.subheader("3️⃣ 특성 중요도 (Feature Importance)")
fig2 = px.bar(
    feature_importance.reset_index(),
    x="index", y=0,
    labels={"index": "특성", "0": "중요도"},
    title="📊 입력 변수 중요도"
)
st.plotly_chart(fig2)
