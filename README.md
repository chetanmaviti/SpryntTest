# checkout-ops-demo-py

A small FastAPI checkout operations service that accepts orders and coordinates core order-processing steps.

## What This App Does

The service exposes a simple order API used by checkout systems:

- Receives orders through POST /orders
- Performs basic duplicate detection by order ID
- Attempts inventory reservation
- Attempts payment charge
- Simulates writing order results to a database layer
- Emits application and incident logs to logs/incident.log

In normal operation, clients can use it to test an order workflow and observe success, duplicate handling, and dependency-failure behavior.

## Quick Start

1. Create and activate virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn app.main:app --reload
```

4. Submit a sample order:

```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H "Content-Type: application/json" \
  -d '{"orderId":"ord_123","userId":"usr_1","amount":149.99,"sku":"SKU-RED-TSHIRT"}'
```

5. Generate demo traffic:

```bash
python scripts/seed_traffic.py
```

## Endpoints

- GET /health
- POST /orders

### POST /orders request body

```json
{
  "orderId": "ord_123",
  "userId": "usr_1",
  "amount": 149.99,
  "sku": "SKU-RED-TSHIRT"
}
```

### POST /orders typical responses

- 200 accepted: order was accepted for processing
- 200 duplicate: order ID was already seen
- 500 or 502: dependency or processing failure paths

## Logs

Application logs are written to logs/incident.log.
