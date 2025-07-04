import streamlit as st

def user_input_form():
    with st.form("prediction_form"):
        alone = st.slider("하루 평균 집에 머무는 시간은 몇 시간인가요?", 0.0, 11.0, 5.0, step=0.5)
        stage_fear = st.radio("사람들 앞에서 발표하거나 무대에 설 때 긴장되거나 두려움을 느끼시나요?", ["Yes", "No"], horizontal=True)
        events = st.slider("최근 1주일 동안 모임이나 활동에 몇 번 참석하셨나요?", 0.0, 10.0, 5.0)
        outside = st.slider("최근 1주일 동안 외출한 횟수는 몇 번인가요?", 0.0, 10.0, 5.0)
        drained = st.radio("사람들과 어울린 뒤 피로감을 느끼는 편인가요?", ["Yes", "No"], horizontal=True)
        friends = st.slider("제일 가깝다고 느끼는 친구는 몇 명 정도 있나요?", 0.0, 15.0, 8.0)
        posts = st.slider("최근 1주일 동안 SNS에 글이나 사진을 몇 번 올리셨나요?", 0.0, 10.0, 5.0)
        submitted = st.form_submit_button("결과!")

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
