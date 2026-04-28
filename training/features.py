import pandas as pd

FEATURE_COLUMNS = [
    "amount",
    "account_age_days",
    "past_txn_count_24h",
    "hour_of_day",
    "merchant_risk_score",
]

TARGET = "is_fraud"


def load_and_prepare_data(path: str):
    df = pd.read_csv(path)

    X = df[FEATURE_COLUMNS]
    y = df[TARGET]

    return X, y
