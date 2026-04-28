# Transaction Risk Scoring ML System

## 1. Problem Overview
This system provides real-time fraud risk scoring for incoming
payment transactions. The output is a probability score used by
downstream services to allow, challenge, or block transactions.

The system is designed to be lightweight, stateless, and low-latency.

---

## 2. Functional Requirements
- Accept transaction features via HTTP API
- Return fraud risk score in real time
- Support threshold-based decisions

---

## 3. Non-Functional Requirements
- P99 latency < 50 ms
- Stateless inference service
- Horizontally scalable
- High availability
- Fault tolerant and observable

---

## 4. Data & Feature Design

### Offline Features
- Merchant risk score
- Historical fraud patterns
- Feature distributions

Computed during offline training and baked into the model.

### Online Features
- Transaction amount
- Hour of day
- Account age
- Recent transaction count

All online features are lightweight and deterministic.

---

## 5. ML Approach
- Binary classification (fraud / not fraud)
- Logistic Regression as baseline
- Probability output used for decisions
- Thresholds controlled outside ML

---

## 6. System Architecture

### Offline Pipeline:
- Data ingestion
- Feature engineering
- Model training
- Model evaluation
- Model versioning via MLflow

### Online Pipeline:
- FastAPI service
- Input validation (Pydantic schemas)
- Feature vector construction
- In-memory model inference
- Async execution for non-blocking performance
- Response generation (JSON)

---

## 7. Offline vs Online Separation
Training and inference code paths are strictly separated to avoid
training-serving skew and accidental coupling.

---

## 8. Decision Logic

The model outputs a probability score using Logistic Regression.

To convert probability into actionable decisions, thresholding is applied:

- **risk_score < 0.25 → allow**
- **0.25 ≤ risk_score < 0.6 → challenge**
- **risk_score ≥ 0.6 → block**

These thresholds are configurable and can be tuned based on business requirements such as fraud tolerance, false positives, and customer experience.

---

## 9. API Design
POST /score

Request:
- Stateless JSON payload
- No user session dependency

Response:
- Risk score
- Decision label
- Model version

---

## 10. Performance Optimizations

### Async Inference
- Model inference executed using async + thread pool
- Prevents blocking of event loop
- Improves concurrency under high load

### Caching Layer
- In-memory caching using TTLCache
- Avoids recomputation for repeated requests
- Reduces latency and CPU usage

---

## 11. Scalability (Conceptual)
- Stateless service enables horizontal scaling
- Load balancer distributes traffic
- Each instance loads model once at startup
- No shared state between instances

---

## 12. Latency Considerations
- Simple model choice (Logistic Regression)
- No database calls in inference path
- Minimal feature transformations
- Model loaded in memory
- Cache reduces repeated computation

---

## 13. Observability & Logging

- Structured JSON logging implemented
- Logs include:
  - timestamp
  - latency
  - risk score
  - decision
  - model version
- Logs stored in JSONL format for easy ingestion into monitoring tools

---

## 14. CI/CD Pipeline

- GitHub Actions used for CI/CD
- Pipeline includes:
  - Dependency installation
  - Linting (flake8)
  - Testing (pytest)
  - Docker image build
  - Container validation
- CD triggered only after successful CI
- Deployment automated via Render webhook

---

## 15. Deployment

- Dockerized FastAPI application
- Containerized environment ensures consistency
- Render used for hosting and deployment
- Auto-deploy triggered from main branch after CI success

---

## 16. Load Testing

- Load tested using Locust
- Simulated:
  - 200 concurrent users
  - ~20,000 requests
- Validated system performance under stress
- Ensured stability and latency targets

---

## 17. Failure Handling
- Invalid input rejected via schema validation
- Model load failure prevents service startup
- Exception handling with structured logging
- API returns proper HTTP error codes

---

## 18. Trade-offs
- Simpler model chosen over deep learning for low latency
- No external feature store to reduce system complexity
- In-memory cache instead of distributed cache (simpler but limited scalability)

---

## 19. Limitations
- No concept drift detection
- No online learning
- Cache is local (not shared across instances)
- No distributed monitoring system

---

## 20. Future Improvements
- Integrate Redis for distributed caching
- Add Prometheus + Grafana for monitoring
- Implement feature store (Feast)
- Canary deployments for model updates
- Add drift detection and alerting