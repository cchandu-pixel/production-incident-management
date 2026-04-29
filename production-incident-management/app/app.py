from flask import Flask, jsonify
import random
import time
import datetime
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# ── Prometheus metrics ──────────────────────────────────────────
REQUEST_COUNT = Counter(
    'app_request_count',
    'Total request count',
    ['endpoint', 'status']
)

RESPONSE_TIME = Histogram(
    'app_response_time_seconds',
    'Response time in seconds',
    ['endpoint']
)

# ── Simulated database of orders ────────────────────────────────
orders = []

# ── Routes ──────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health_check():
    REQUEST_COUNT.labels(endpoint='/health', status='200').inc()
    return jsonify({
        "status": "healthy",
        "timestamp": str(datetime.datetime.now())
    }), 200


@app.route('/orders', methods=['GET'])
def get_orders():
    start = time.time()

    # Simulate random slow response (production issue)
    if random.random() < 0.2:
        time.sleep(3)

    duration = time.time() - start
    RESPONSE_TIME.labels(endpoint='/orders').observe(duration)

    # Simulate random errors (production issue)
    if random.random() < 0.15:
        REQUEST_COUNT.labels(endpoint='/orders', status='500').inc()
        return jsonify({
            "error": "Internal Server Error",
            "timestamp": str(datetime.datetime.now())
        }), 500

    REQUEST_COUNT.labels(endpoint='/orders', status='200').inc()
    return jsonify({
        "orders": orders,
        "total": len(orders),
        "timestamp": str(datetime.datetime.now())
    }), 200


@app.route('/orders/create', methods=['POST'])
def create_order():
    start = time.time()

    # Simulate random errors
    if random.random() < 0.1:
        REQUEST_COUNT.labels(endpoint='/orders/create', status='500').inc()
        return jsonify({
            "error": "Failed to create order",
            "timestamp": str(datetime.datetime.now())
        }), 500

    order = {
        "id": len(orders) + 1,
        "product": random.choice(["Laptop", "Phone", "Tablet", "Monitor"]),
        "status": "created",
        "timestamp": str(datetime.datetime.now())
    }
    orders.append(order)

    duration = time.time() - start
    RESPONSE_TIME.labels(endpoint='/orders/create').observe(duration)
    REQUEST_COUNT.labels(endpoint='/orders/create', status='200').inc()

    return jsonify({
        "message": "Order created successfully",
        "order": order
    }), 200


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


# ── Run ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)