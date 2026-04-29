import sqlite3
import json
import datetime
import os

# ── Database setup ───────────────────────────────────────────────
DB_PATH = "docs/incidents.db"

def init_database():
    os.makedirs("docs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            status INTEGER NOT NULL,
            message TEXT NOT NULL,
            severity TEXT NOT NULL,
            resolved TEXT DEFAULT 'NO'
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# ── Save incident ────────────────────────────────────────────────
def log_incident(endpoint, status, message, severity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO incidents (timestamp, endpoint, status, message, severity)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        str(datetime.datetime.now()),
        endpoint,
        status,
        message,
        severity
    ))
    conn.commit()
    conn.close()
    print(f"✅ Incident saved to database!")

# ── Get all incidents ────────────────────────────────────────────
def get_all_incidents():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM incidents ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── Get incidents by severity ────────────────────────────────────
def get_incidents_by_severity(severity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM incidents WHERE severity = ? ORDER BY timestamp DESC',
        (severity,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

# ── Resolve incident ─────────────────────────────────────────────
def resolve_incident(incident_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE incidents SET resolved = ? WHERE id = ?',
        ('YES', incident_id)
    )
    conn.commit()
    conn.close()
    print(f"✅ Incident {incident_id} marked as resolved!")

# ── Print incident report ────────────────────────────────────────
def print_report():
    incidents = get_all_incidents()
    print("\n" + "=" * 60)
    print("📊 INCIDENT REPORT")
    print("=" * 60)
    print(f"Total incidents: {len(incidents)}")

    high = [i for i in incidents if i[5] == 'HIGH']
    low  = [i for i in incidents if i[5] == 'LOW']

    print(f"🔴 HIGH severity: {len(high)}")
    print(f"🟡 LOW severity:  {len(low)}")
    print("=" * 60)

    for incident in incidents:
        print(f"\nID:        {incident[0]}")
        print(f"Time:      {incident[1]}")
        print(f"Endpoint:  {incident[2]}")
        print(f"Status:    {incident[3]}")
        print(f"Message:   {incident[4]}")
        print(f"Severity:  {incident[5]}")
        print(f"Resolved:  {incident[6]}")
        print("-" * 40)

# ── Main ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    init_database()

    print("\n📝 Logging test incidents...")
    log_incident("/orders", 500, "Internal Server Error", "HIGH")
    log_incident("/orders", 200, "Slow response: 3.00s", "LOW")
    log_incident("/health", 500, "Health check failed", "HIGH")

    print("\n✅ Resolving first incident...")
    resolve_incident(1)

    print_report()