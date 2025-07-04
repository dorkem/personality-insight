import streamlit as st
import matplotlib.pyplot as plt
from ui.forms import user_input_form
from model.predictor import predict_personality
import seaborn as sns

def main_tab(accuracy, report, df, feature_importance):
    # 성격 유형 분포 - 막대그래프
    st.subheader("📊 성격 유형 분포")
    personality_counts = df["PERSONALITY"].value_counts().reindex(["Introvert", "Extrovert"], fill_value=0)
    colors = ["#A0522D", "#6B8E23"]  # Introvert: 갈색, Extrovert: 초록색
    fig, ax = plt.subplots()
    ax.bar(personality_counts.index, personality_counts.values, color=colors)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    # 성격 그룹 분리
    df["PERSONALITY"] = df["PERSONALITY"].str.strip()
    introvert_df = df[df["PERSONALITY"] == "Introvert"]
    extrovert_df = df[df["PERSONALITY"] == "Extrovert"]

    # 이진 특성 - 원형그래프
    st.subheader("🧠 사회적 상황에서의 반응 ")
    binary_columns = ["STAGE_FEAR", "DRAINED_AFTER_SOCIALIZING"]

    for feature in binary_columns:
        st.markdown(
            f"<h4 style='text-align: center;'>💬 {feature.replace('_', ' ').title()}</h3>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            series = introvert_df[feature].value_counts().reindex(["Yes", "No"], fill_value=0)
            if series.sum() == 0:
                st.warning("데이터 없음")
            else:
                fig, ax = plt.subplots()
                series.plot.pie(labels=["Yes", "No"], autopct="%1.1f%%", startangle=90,
                                colors=["#A0522D", "#D2B48C"], ax=ax)  # 갈색 & 베이지
                ax.set_ylabel("")
                st.pyplot(fig)
            st.markdown("<p style='text-align: center;'>Introvert</p>", unsafe_allow_html=True)

        with col2:
            series = extrovert_df[feature].value_counts().reindex(["Yes", "No"], fill_value=0)
            if series.sum() == 0:
                st.warning("데이터 없음")
            else:
                fig, ax = plt.subplots()
                series.plot.pie(labels=["Yes", "No"], autopct="%1.1f%%", startangle=90,
                                colors=["#6B8E23", "#B0C4B1"], ax=ax)  # 초록 & 연두그레이
                ax.set_ylabel("")
                st.pyplot(fig)
            st.markdown("<p style='text-align: center;'>Extrovert</p>", unsafe_allow_html=True)

    # 연속형 특성 - 박스플롯
    st.subheader("🎨 성격 유형별 연속형 특성 분포")
    numeric_columns = [
        "TIME_SPENT_ALONE", "SOCIAL_EVENT_ATTENDANCE",
        "GOING_OUTSIDE", "FRIENDS_CIRCLE_SIZE", "POST_FREQUENCY"
    ]

    sns.set(style="whitegrid", font_scale=0.9)
    custom_palette = {"Introvert": "#A0522D", "Extrovert": "#6B8E23"}  # 가을톤 색상

    fig = plt.figure(figsize=(12, 10))
    for i, col in enumerate(numeric_columns, 1):
        plt.subplot(3, 2, i)
        ax = sns.boxplot(
            x="PERSONALITY", hue="PERSONALITY", y=col, data=df,
            palette=custom_palette, legend=False,
            width=0.6, fliersize=3, linewidth=1.5
        )
        ax.set_title(f'{col.replace("_", " ").title()} by Personality', fontsize=11, weight='bold')
        ax.set_xlabel("")
        ax.set_ylabel(col.replace("_", " ").title(), fontsize=10)

    plt.tight_layout()
    st.pyplot(fig)

    # 모델 정확도 및 리포트
    st.subheader("📈 성격 분석 대시보드")
    st.write(f"✅ 모델 정확도: **{accuracy:.2f}**")
    st.code(report)

    # 중요 특성 그래프
    st.subheader("🎯 중요 특성 (Feature Importance)")
    fig_feat, ax_feat = plt.subplots()
    feature_importance.plot(kind='bar', ax=ax_feat, color="#6B8E23")  # Extrovert 색으로 맞춤
    st.pyplot(fig_feat)
                

def survey_tab(model):
    st.title("📝 성향 분석")

    input_dict = user_input_form()
    if input_dict:
        pred, proba = predict_personality(model, input_dict)
        label = "Extrovert" if pred == 1 else "Introvert"
        st.success(f"🧠 예측된 성격 유형: **{label}**")
        st.progress(int(proba[pred] * 100), text=f"{label} 확률: {proba[pred]*100:.2f}%")

