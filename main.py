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

st.subheader("4️⃣ 사용자 행동 데이터로 성격 예측하기")

# 사용자 입력 받기
with st.form("prediction_form"):
    st.write("🧑 당신의 행동을 입력해보세요:")
    alone = st.slider("혼자 있는 시간 (시간)", 0.0, 12.0, 4.0, step=0.5)
    stage_fear = st.selectbox("무대 공포감이 있나요?", ["No", "Yes"])
    events = st.slider("사회적 모임 참석 횟수", 0.0, 10.0, 5.0)
    outside = st.slider("외출 횟수", 0.0, 10.0, 5.0)
    drained = st.selectbox("사회활동 후 피곤함을 느끼나요?", ["No", "Yes"])
    friends = st.slider("친구 수", 0.0, 20.0, 8.0)
    posts = st.slider("SNS 게시 빈도", 0.0, 10.0, 5.0)

    submitted = st.form_submit_button("성격 예측")

# 입력을 바탕으로 예측
if submitted:
    input_df = pd.DataFrame([{
        "TIME_SPENT_ALONE": alone,
        "STAGE_FEAR": 1 if stage_fear == "Yes" else 0,
        "SOCIAL_EVENT_ATTENDANCE": events,
        "GOING_OUTSIDE": outside,
        "DRAINED_AFTER_SOCIALIZING": 1 if drained == "Yes" else 0,
        "FRIENDS_CIRCLE_SIZE": friends,
        "POST_FREQUENCY": posts
    }])

    prediction = model.predict(input_df)[0]
    pred_label = "Extrovert" if prediction == 1 else "Introvert"

    st.success(f"🧠 예측된 성격 유형: **{pred_label}**")

    # 예측 결과 및 확률
    prediction = model.predict(input_df)[0]
    pred_label = "Extrovert" if prediction == 1 else "Introvert"
    proba = model.predict_proba(input_df)[0]

    introvert_prob = proba[0] * 100
    extrovert_prob = proba[1] * 100

    st.success(f"🧠 예측된 성격 유형: **{pred_label}**")
    st.write(f"🔍 내향적일 확률: **{introvert_prob:.1f}%**, 외향적일 확률: **{extrovert_prob:.1f}%**")

    # 원형 차트 표시 (Pie Chart)
    pie_df = pd.DataFrame({
        "성격 유형": ["Introvert", "Extrovert"],
        "확률 (%)": [introvert_prob, extrovert_prob]
    })

    fig_pie = px.pie(pie_df, names="성격 유형", values="확률 (%)",
                     title="🧠 성격 예측 확률 분포", color="성격 유형",
                     color_discrete_map={"Introvert": "#636EFA", "Extrovert": "#EF553B"})
    fig_pie.update_traces(textinfo="label+percent")
    st.plotly_chart(fig_pie)

    # 간단한 코칭 문구
    if pred_label == "Introvert":
        st.info("💬 혼자 있는 시간이 중요합니다. 너무 고립되지 않게 작은 만남을 시도해보세요.")
    else:
        st.info("💬 사람들과의 교류에서 에너지를 얻는 스타일입니다. 하지만 무리한 스케줄은 피해주세요.")

