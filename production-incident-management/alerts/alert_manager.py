import requests
import time
import datetime
import json

# ── Config ──────────────────────────────────────────────────────
FLASK_URL = "http://127.0.0.1:5000"
CHECK_INTERVAL = 10  # check every 10 seconds
ERROR_THRESHOLD = 2  # alert after 2 consecutive failures

# ── Alert counter ───────────────────────────────────────────────
consecutive_failures = 0

# ── Log incident to file ─────────────────────────────────────────
def log_incident(endpoint, status, message):
    incident = {
        "timestamp": str(datetime.datetime.now()),
        "endpoint": endpoint,
        "status": status,
        "message": message,
        "severity": "HIGH" if status == 500 else "LOW"
    }
    with open("docs/incidents.json", "a") as f:
        f.write(json.dumps(incident) + "\n")
    print(f"🚨 INCIDENT LOGGED: {incident}")

# ── Check health ─────────────────────────────────────────────────
def check_health():
    try:
        response = requests.get(f"{FLASK_URL}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ [{datetime.datetime.now()}] Health check PASSED")
            return True
        else:
            print(f"❌ [{datetime.datetime.now()}] Health check FAILED - {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ [{datetime.datetime.now()}] Health check ERROR - {str(e)}")
        return False

# ── Check orders endpoint ────────────────────────────────────────
def check_orders():
    try:
        start = time.time()
        response = requests.get(f"{FLASK_URL}/orders", timeout=5)
        duration = time.time() - start

        if response.status_code == 500:
            log_incident("/orders", 500, "Orders endpoint returned 500 error")
            return False

        if duration > 2:
            log_incident("/orders", 200, f"Slow response detected: {duration:.2f}s")
            print(f"⚠️  [{datetime.datetime.now()}] Slow response: {duration:.2f}s")
            return False

        print(f"✅ [{datetime.datetime.now()}] Orders check PASSED - {duration:.2f}s")
        return True

    except Exception as e:
        log_incident("/orders", 500, f"Orders endpoint ERROR: {str(e)}")
        return False

# ── Main monitoring loop ─────────────────────────────────────────
def run_monitor():
    global consecutive_failures
    print("🚀 Alert Manager Started - Monitoring every 10 seconds")
    print("=" * 60)

    while True:
        health_ok = check_health()
        orders_ok = check_orders()

        if not health_ok or not orders_ok:
            consecutive_failures += 1
            print(f"⚠️  Consecutive failures: {consecutive_failures}")

            if consecutive_failures >= ERROR_THRESHOLD:
                print("🚨 ALERT THRESHOLD REACHED - Incident logged!")
                consecutive_failures = 0
        else:
            consecutive_failures = 0

        print("-" * 60)
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    run_monitor()