# checkout-ops-demo-py

A small FastAPI service intentionally seeded with simple production incidents for Sprynt demos.

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

## Logs

Application logs are written to logs/incident.log.

## Intentional Incidents

See INCIDENT_CATALOG.md for the list of intentionally vulnerable behaviors included for detection demonstrations.
