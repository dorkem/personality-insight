import pandas as pd

def predict_personality(model, input_data: dict):
    df = pd.DataFrame([input_data])
    pred = model.predict(df)[0]
    proba = model.predict_proba(df)[0]
    return pred, proba
