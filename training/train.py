import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from features import load_and_prepare_data
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train():
    X, y = load_and_prepare_data("data/raw/transactions.csv")

    # Ensure feature names are set (required for sklearn compatibility)
    FEATURE_NAMES = [
        "amount",
        "account_age_days",
        "past_txn_count_24h",
        "hour_of_day",
        "merchant_risk_score",
    ]

    if isinstance(X, pd.DataFrame):
        X.columns = FEATURE_NAMES
    else:
        X = pd.DataFrame(X, columns=FEATURE_NAMES)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    base_model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    model = CalibratedClassifierCV(base_model, method="sigmoid", cv=3)

    with mlflow.start_run():
        model.fit(X_train, y_train)

        preds = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, preds)

        mlflow.log_metric("roc_auc", auc)
        mlflow.sklearn.log_model(model, "logreg_v1")

        print(f"ROC-AUC: {auc:.4f}")

    joblib.dump(model, "models/logreg_v1.pkl")


if __name__ == "__main__":
    train()
