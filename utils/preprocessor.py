import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["STAGE_FEAR"] = df["STAGE_FEAR"].map({"Yes": 1, "No": 0})
    df["DRAINED_AFTER_SOCIALIZING"] = df["DRAINED_AFTER_SOCIALIZING"].map({"Yes": 1, "No": 0})
    df["PERSONALITY"] = df["PERSONALITY"].map({"Extrovert": 1, "Introvert": 0})
    return df