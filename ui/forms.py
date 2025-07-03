import streamlit as st

def user_input_form():
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

    if submitted:
        input_dict = {
            "TIME_SPENT_ALONE": alone,
            "STAGE_FEAR": 1 if stage_fear == "Yes" else 0,
            "SOCIAL_EVENT_ATTENDANCE": events,
            "GOING_OUTSIDE": outside,
            "DRAINED_AFTER_SOCIALIZING": 1 if drained == "Yes" else 0,
            "FRIENDS_CIRCLE_SIZE": friends,
            "POST_FREQUENCY": posts
        }
        return input_dict
    return None
