from fastapi import FastAPI, HTTPException
from utils.logger import get_logger
import logging
import json
import time
import warnings
from cachetools import TTLCache
import numpy as np
import pandas as pd
from datetime import datetime
import asyncio
import warnings

from inference.schemas import TransactionRequest, RiskResponse
from inference.model_loader import load_model, FEATURE_NAMES

# -----------------------
# Setup Logging
# -----------------------

logger = get_logger()

# -----------------------
# Setup Cache (5 min TTL)
# -----------------------
cache = TTLCache(maxsize=1000, ttl=300)

app = FastAPI(
    title="Transaction Risk Assessment API",
    description="ML-powered transaction risk scoring and decision engine",
    version="1.0.0"
)
model = load_model()


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and load balancing"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "model_loaded": model is not None
    }


@app.get("/metadata")
def get_metadata():
    """Retrieve API and model metadata"""
    return {
        "api_version": "1.0.0",
        "model_version": "logreg_v1",
        "model_type": "LogisticRegression",
        "features": [
            "amount",
            "account_age_days",
            "past_txn_count_24h",
            "hour_of_day",
            "merchant_risk_score"
        ],
        "decision_thresholds": {
            "allow": "< 0.25",
            "challenge": "0.25 - 0.6",
            "block": "> 0.6"
        },
        "last_updated": "2026-02-08"
    }


@app.post("/score", response_model=RiskResponse)
async def score_transaction(req: TransactionRequest):
    start_time = time.time()

    try:
        # -----------------------
        # Create cache key
        # -----------------------
        key = json.dumps(req.dict(), sort_keys=True)

        # -----------------------
        # Check cache
        # -----------------------
        if key in cache:
            logger.info("Cache HIT")
            return RiskResponse(
                risk_score=float(cache[key]["risk_score"]),
                decision=cache[key]["decision"],
                model_version="logreg_v1"
            )

        logger.info("Cache MISS")

        # -----------------------
        # Prepare features
        # -----------------------
        features = pd.DataFrame([{
            "amount": req.amount,
            "account_age_days": req.account_age_days,
            "past_txn_count_24h": req.past_txn_count_24h,
            "hour_of_day": req.hour_of_day,
            "merchant_risk_score": req.merchant_risk_score
        }])

        features = features[FEATURE_NAMES]

        # -----------------------
        # Async model inference
        # -----------------------
        loop = asyncio.get_running_loop()

        def predict():
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                return model.predict_proba(features)[0][1]

        risk_score = await loop.run_in_executor(None, predict)

        # -----------------------
        # Business logic
        # -----------------------
        if risk_score < 0.25:
            decision = "allow"
        elif risk_score < 0.6:
            decision = "challenge"
        else:
            decision = "block"

        # -----------------------
        # Store in cache
        # -----------------------
        cache[key] = {
            "risk_score": float(risk_score),
            "decision": decision
        }

        # -----------------------
        # Logging
        # -----------------------
        latency = round((time.time() - start_time) * 1000, 2)
        logger.info(
            "request_processed",
            extra={
                "extra_data": {
                    "risk_score": float(risk_score),
                    "decision": decision,
                    "latency_ms": latency,
                    "model_version": "logreg_v1",
                    "input_amount": req.amount  # 
                }
            }
        )

        # -----------------------
        # Response
        # -----------------------
        return RiskResponse(
            risk_score=float(risk_score),
            decision=decision,
            model_version="logreg_v1"
        )

    except Exception as e:
        logger.error(
            "error_occurred",
            extra={"extra_data": {"error": str(e)}}
        )
        raise HTTPException(status_code=500, detail=str(e))