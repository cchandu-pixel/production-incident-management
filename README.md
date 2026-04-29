# 🚨 Production Incident Management System

A real-world production monitoring system built with Python, Flask, 
Prometheus, Grafana and Docker — simulating how companies like 
Amazon, Microsoft and Google monitor their live systems 24/7.

---

## 🎯 What This Project Does

- Runs a **live Flask production app** with real API endpoints
- **Automatically detects incidents** — slow responses, errors, downtime
- **Logs every incident** into a SQLite database with severity levels
- **Fires alerts** when error threshold is reached
- **Displays live metrics** on a Grafana dashboard
- **Runs everything** with a single Docker command

---

## 🏗️ Architecture

Flask App (Port 5000)
↓ exposes metrics
Prometheus (Port 9090)
↓ scrapes metrics
Grafana (Port 3000)
↓ displays dashboard
Alert Manager
↓ monitors Flask app
Incident Logger
↓ saves to SQLite database

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python + Flask | Production app simulation |
| Prometheus | Metrics collection |
| Grafana | Live monitoring dashboard |
| SQLite | Incident database |
| Docker + Docker Compose | Container orchestration |
| GitHub Actions | CI/CD pipeline |

---

## 🚀 How To Run

### Prerequisites
- Docker Desktop installed
- Python 3.11+

### Run with Docker (recommended)
```bash
# Clone the repo
git clone https://github.com/cchandu-pixel/production-incident-management.git

# Go into the folder
cd production-incident-management

# Start everything with one command
docker-compose up --build
```

### Access the services
| Service | URL |
|---|---|
| Flask App | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

### Grafana Login

Username: admin
Password: admin123

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check |
| `/orders` | GET | Get all orders (simulates random failures) |
| `/orders/create` | POST | Create new order |
| `/metrics` | GET | Prometheus metrics |

---

## 🚨 How Incident Detection Works

1. Alert Manager checks Flask app every **10 seconds**
2. If response time exceeds **2 seconds** → incident logged
3. If endpoint returns **500 error** → incident logged
4. If **2 consecutive failures** → alert threshold reached
5. Every incident saved to **SQLite database** with severity level

---

## 📁 Project Structure

production-incident-management/
📂 app/
📄 app.py              ← Flask production app
📂 alerts/
📄 alert_manager.py    ← Alert detection system
📂 logger/
📄 incident_logger.py  ← SQLite incident database
📂 docs/
📄 incidents.json      ← Incident log file
📄 incidents.db        ← SQLite database
📄 docker-compose.yml   ← Runs everything together
📄 Dockerfile           ← Flask app container
📄 prometheus.yml       ← Prometheus config
📄 requirements.txt     ← Python dependencies

---

## 💡 Key Skills Demonstrated

- ✅ Production system monitoring
- ✅ Incident detection and alerting
- ✅ Database logging and reporting
- ✅ Containerization with Docker
- ✅ Metrics collection with Prometheus
- ✅ Dashboard visualization with Grafana
- ✅ Python scripting and automation
- ✅ RESTful API development

---

## 👨‍💻 Author

Built by **Chandu** as part of a Production Support Engineer portfolio project.

Connect on LinkedIn: https://www.linkedin.com/in/chandu-ch