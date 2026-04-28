[![CI](https://github.com/Nithin00614/Transaction-Risk-Scoring-System/actions/workflows/ci.yml/badge.svg)](https://github.com/Nithin00614/Transaction-Risk-Scoring-System)

![Python](https://img.shields.io/badge/Python-3.11-blue)

![API](https://img.shields.io/badge/API-FastAPI-green)

![Latency](https://img.shields.io/badge/Latency-sub--150ms-brightgreen)

![Throughput](https://img.shields.io/badge/Throughput-160RPS-blue)

![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

![Render](https://img.shields.io/badge/Deployed-Render-purple)

![License](https://img.shields.io/badge/License-MIT-yellow)


### Transaction Risk ML – Real-Time Risk Scoring System

## Overview

This project implements a real-time transaction risk scoring system using machine learning.

It predicts the fraud risk probability of a transaction and maps it into actionable decisions:

- ALLOW → Low risk
- CHALLENGE → Medium risk
- BLOCK → High risk

The system follows a production-style ML workflow with clearly separated training and inference pipelines.

---

## Key Features

- End-to-end ML pipeline (training → inference)
- Real-time inference using FastAPI
- CI/CD integration with automated testing
- Dockerized deployment
- Structured logging (captured via cloud platform)
- Scenario-based validation for risk decisions

---

## Model Summary

- Model: Logistic Regression
- Preprocessing: StandardScaler
- Training Data: Synthetic dataset with realistic fraud patterns
- ROC-AUC: ~0.93

The model outputs a risk probability, which is converted into business decisions using thresholding.

---

## Project Structure

transaction-risk-ml/
│
├── data/
├── training/            # Training pipeline
├── inference/           # API & inference logic
├── models/              # Model artifacts
├── system_design.md     # Architecture documentation
├── requirements.txt
├── Dockerfile
└── README.md

---

## Running the Project

Install dependencies

pip install -r requirements.txt

Train model

python training/train.py

Run inference API

uvicorn inference.app:app --reload

API:

http://127.0.0.1:8000/docs

---

## 🌐 Live API

The model is deployed and accessible via a public API.

- Base URL
  https://transaction-risk-ml-production-system.onrender.com

- Swagger UI
  https://transaction-risk-ml-production-system.onrender.com/docs

---

Example Request

{
  "amount": 2500,
  "account_age_days": 180,
  "past_txn_count_24h": 5,
  "hour_of_day": 22,
  "merchant_risk_score": 0.5
}

---

Example Response

{
  "risk_score": 0.47,
  "decision": "CHALLENGE"
}

---

## ⚡ Performance & Load Testing

The system was evaluated under simulated load to validate real-time performance.

- Tool Used: Locust
- Throughput: ~160 requests/second
- Latency: <150 ms (average)
- Failure Rate: 0% under sustained load

These results demonstrate the system’s ability to handle high-throughput, low-latency inference workloads.

---

## Deployment

docker build -t <username>/transaction-risk-ml .
docker run -p 10000:10000 <username>/transaction-risk-ml

The API is deployed on Render with logs streamed via stdout and monitored through the platform dashboard.

---

## Dataset

The dataset used for training is synthetic and not included in this repository.

It simulates real-world fraud scenarios using:

- Transaction behavior
- Account characteristics
- Merchant risk signals

---

## Model Performance

- Model: Logistic Regression
- ROC-AUC Score: ~0.93
- Pipeline: StandardScaler + Logistic Regression

---

## Documentation

For detailed architecture, design decisions, and trade-offs:

➡️ *Detailed System Design*  
  → [Open](system_design.md)

---