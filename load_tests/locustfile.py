import random

from locust import HttpUser, between, task


class TransactionUser(HttpUser):
    host = "http://127.0.0.1:8000"  # local testing
    wait_time = between(0.5, 1.5)  # realistic user delay

    def generate_payload(self):
        return {
            "amount": random.randint(100, 5000),
            "account_age_days": random.randint(0, 3650),
            "past_txn_count_24h": random.randint(0, 50),
            "hour_of_day": random.randint(0, 23),
            "merchant_risk_score": round(random.uniform(0, 1), 2),
        }

    @task
    def score(self):
        payload = self.generate_payload()
        self.client.post("/score", json=payload, timeout=10)
