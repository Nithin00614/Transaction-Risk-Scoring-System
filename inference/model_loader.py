import warnings

import joblib

MODEL_PATH = "models/logreg_v1.pkl"

model = None

# Feature names that the model expects
FEATURE_NAMES = [
    "amount",
    "account_age_days",
    "past_txn_count_24h",
    "hour_of_day",
    "merchant_risk_score",
]


def load_model():
    global model
    if model is None:
        # Suppress sklearn feature name warnings during load
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            model = joblib.load(MODEL_PATH)
    return model
