import streamlit as st

from utils.snowflake_setup import get_session, initialize_snowflake_environment
from data.loader import load_data
from utils.preprocessor import preprocess
from model.trainer import PersonalityModel
from model.predictor import predict_personality
from ui.forms import user_input_form

session = get_session()
# initialize_snowflake_environment(session)
df_raw = load_data(session, "personality_survey")
df_processed = preprocess(df_raw)

# 학습
modeler = PersonalityModel(df_processed)
modeler.train()
accuracy, report = modeler.evaluate()
feature_importance = modeler.get_feature_importance()
model = modeler.get_model()

# UI
st.title("🧠 성격 예측 서비스")
st.write(f"✅ 모델 정확도: {accuracy:.2f}")
st.code(report)

# 사용자 입력
input_dict = user_input_form()
if input_dict:
    pred, proba = predict_personality(model, input_dict)
    label = "Extrovert" if pred == 1 else "Introvert"
    st.success(f"🧠 예측된 성격 유형: **{label}**")
