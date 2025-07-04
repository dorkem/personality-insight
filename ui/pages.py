import streamlit as st
import matplotlib.pyplot as plt
from ui.forms import user_input_form
from model.predictor import predict_personality

def main_tab(accuracy, report, df, feature_importance):
    # ✅ 정확도 및 리포트 먼저
    st.title("📈 성격 분석 대시보드")
    st.write(f"✅ 모델 정확도: **{accuracy:.2f}**")
    st.code(report)

    # ✅ 성격 그룹 분리
    df["PERSONALITY"] = df["PERSONALITY"].str.strip()
    introvert_df = df[df["PERSONALITY"] == "Introvert"]
    extrovert_df = df[df["PERSONALITY"] == "Extrovert"]

    # ✅ 중요 특성 그래프
    st.subheader("🎯 중요 특성 (Feature Importance)")
    fig_feat, ax_feat = plt.subplots()
    feature_importance.plot(kind='bar', ax=ax_feat)
    st.pyplot(fig_feat)

    # ✅ 이진 특성 - 원형그래프
    st.subheader("🧠 이진 특성 (Yes/No) 원형 그래프")
    binary_columns = ["STAGE_FEAR", "DRAINED_AFTER_SOCIALIZING"]
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧍‍♂️ Introvert")
        # pie chart 시각화: Yes/No 기준 그대로 계산
        for feature in binary_columns:
            series = introvert_df[feature].value_counts().reindex(["Yes", "No"], fill_value=0)

            if series.sum() == 0:
                st.warning(f"{feature}에 대한 데이터가 없습니다.")
                continue

            fig, ax = plt.subplots()
            series.plot.pie(
                labels=["Yes", "No"],
                autopct="%1.1f%%",
                startangle=90,
                ax=ax
            )
            ax.set_ylabel("")
            ax.set_title(feature.replace("_", " ").title())
            st.pyplot(fig)


    with col2:
        st.markdown("### 🧑‍🤝‍🧑 Extrovert")
        for feature in binary_columns:
            series = extrovert_df[feature].value_counts().reindex(["Yes", "No"], fill_value=0)
            if series.sum() == 0:
                st.warning(f"{feature}에 대한 데이터가 없습니다.")
                continue
            fig, ax = plt.subplots()
            series.plot.pie(
                labels=["Yes", "No"],
                autopct="%1.1f%%",
                startangle=90,
                ax=ax
            )
            ax.set_ylabel("")
            ax.set_title(feature.replace("_", " ").title())
            st.pyplot(fig)

    # ✅ 연속형 특성 - 평균 막대그래프
    st.subheader("📊 연속형 특성 평균 비교")
    numeric_columns = [
        "TIME_SPENT_ALONE", "SOCIAL_EVENT_ATTENDANCE",
        "GOING_OUTSIDE", "FRIENDS_CIRCLE_SIZE", "POST_FREQUENCY"
    ]

    for i in range(0, len(numeric_columns), 2):  # 2개씩 나눠서 가로 정렬
        with st.container():
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(numeric_columns):
                    feature = numeric_columns[i + j]
                    with cols[j]:
                        intro_mean = introvert_df[feature].mean()
                        extro_mean = extrovert_df[feature].mean()
                        fig, ax = plt.subplots()
                        ax.bar(["Introvert", "Extrovert"], [intro_mean, extro_mean])
                        ax.set_title(feature.replace("_", " ").title())
                        st.pyplot(fig)

def survey_tab(model):
    st.title("📝 당신의 성격을 예측해보세요!")

    input_dict = user_input_form()
    if input_dict:
        pred, proba = predict_personality(model, input_dict)
        label = "Extrovert" if pred == 1 else "Introvert"
        st.success(f"🧠 예측된 성격 유형: **{label}**")
        st.progress(int(proba[pred] * 100), text=f"{label} 확률: {proba[pred]*100:.2f}%")

