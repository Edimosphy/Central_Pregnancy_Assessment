import joblib
import pandas as pd

def save_model(model):
    with open("maternal_risk_model.pkl", "wb") as f:
        joblib.dump(model, f)

def load_model():
    with open("maternal_risk_model.pkl", "rb") as f:
        return joblib.load(f)

def predict_risk(record_dict):
    model = load_model()
    try:
        df = pd.DataFrame([record_dict])
        # Align columns to model's expected features if possible
        if hasattr(model, 'feature_names_in_'):
            df = df.reindex(columns=model.feature_names_in_, fill_value=0)
        prediction = model.predict(df)[0]
    except Exception as e:
        prediction = f"Error in prediction: {e}"
    return prediction
