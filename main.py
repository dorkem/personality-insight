import streamlit as st

from utils.snowflake_setup import get_session, initialize_snowflake_environment
from data.loader import load_data
from utils.preprocessor import preprocess
from model.trainer import PersonalityModel
from ui import pages

session = get_session()
# initialize_snowflake_environment(session)
df = load_data(session, "personality_survey")
df_processed = preprocess(df)

df_viz = df.copy()
for col in ["PERSONALITY", "STAGE_FEAR", "DRAINED_AFTER_SOCIALIZING"]:
    df_viz[col] = df_viz[col].astype(str).str.strip()

# 학습
modeler = PersonalityModel(df_processed)
modeler.train()
accuracy, report = modeler.evaluate()
feature_importance = modeler.get_feature_importance()
model = modeler.get_model()

# UI
tab1, tab2 = st.tabs(["📊 분석 대시보드", "📝 성격 설문 및 예측"])

with tab1:
    pages.main_tab(accuracy, report, df_viz, feature_importance)

with tab2:
    pages.survey_tab(model)