import numpy as np
import pandas as pd

np.random.seed(42)

N = 100_000

# -------------------------------
# 1. Generate Base Features
# -------------------------------

amount = np.random.exponential(scale=2000, size=N)
account_age_days = np.random.randint(1, 2000, size=N)
past_txn_count_24h = np.random.poisson(3, size=N)
hour_of_day = np.random.randint(0, 24, size=N)
merchant_risk_score = np.random.uniform(0, 1, size=N)

df = pd.DataFrame(
    {
        "amount": amount,
        "account_age_days": account_age_days,
        "past_txn_count_24h": past_txn_count_24h,
        "hour_of_day": hour_of_day,
        "merchant_risk_score": merchant_risk_score,
    }
)

# -------------------------------
# 2. Feature Engineering
# -------------------------------

# Normalize continuous features
amount_norm = np.log1p(amount) / 10
txn_norm = past_txn_count_24h / 20

# Behavioral signals
night_risk = ((hour_of_day >= 0) & (hour_of_day <= 5)).astype(int)
new_account_risk = (account_age_days < 100).astype(int)

# Non-linear signals (VERY IMPORTANT)
high_amount_flag = (amount > 5000).astype(int)
high_txn_flag = (past_txn_count_24h > 10).astype(int)

# -------------------------------
# 3. Fraud Score (STRONG SIGNAL)
# -------------------------------

fraud_score = (
    1.2 * amount_norm
    + 0.8 * txn_norm
    + 1.5 * merchant_risk_score
    + 0.7 * night_risk
    + 0.7 * new_account_risk
    + 0.8 * high_amount_flag
    + 0.8 * high_txn_flag
    + np.random.normal(0, 0.15, size=N)  # noise
)

# -------------------------------
# 4. Convert to Probability
# -------------------------------

fraud_prob = 1 / (1 + np.exp(-fraud_score))

# Prevent extreme 0/1 probabilities
fraud_prob = 0.05 + 0.9 * fraud_prob  # range ~0.05–0.95

# -------------------------------
# 5. Control Fraud Rate (~25%)
# -------------------------------

TARGET_FRAUD_RATE = 0.25

threshold = np.quantile(fraud_prob, 1 - TARGET_FRAUD_RATE)

df["is_fraud"] = (fraud_prob > threshold).astype(int)

# -------------------------------
# 6. Save Dataset
# -------------------------------

df.to_csv("data/raw/transactions.csv", index=False)

print(" Improved dataset generated:", df.shape)
print(df["is_fraud"].value_counts(normalize=True))
