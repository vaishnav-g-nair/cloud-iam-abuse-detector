# ☁️ Cloud IAM Abuse Detector (Demo Project)

A **detection-engineering demo project** that simulates Cloud IAM activity, detects suspicious identity abuse patterns, and presents findings in an analyst-friendly format (CLI + Web UI).

> ⚠️ **Note:**
> This project is **for learning, demos, and security interviews only**.
> It is **not production-ready** and does **not replace cloud-native security tools**.

---

## 🎯 Why This Project Exists

Identity and access abuse is one of the **most common cloud attack vectors**:

* Compromised credentials
* Suspicious login locations
* Rapid privilege escalation
* Brute-force attempts

This project demonstrates **how a detection engineer thinks**:

* Simulating realistic IAM logs
* Writing rule-based detections
* Producing evidence-driven alerts
* Presenting results clearly for analysts

---

## 🧠 What This Project Demonstrates

* IAM log simulation for demos
* Rule-based anomaly detection
* Evidence-focused alerting
* Separation of detection, reporting, and UI
* Analyst-friendly presentation (CLI + Web)

---

## 🔍 Detection Rules Implemented

| Rule                       | Description                                          | Severity |
| -------------------------- | ---------------------------------------------------- | -------- |
| Unusual Login Location     | Login from high-risk country deviating from baseline | High     |
| Multiple Failed Logins     | Brute-force style login attempts                     | High     |
| Rapid Privilege Escalation | Fast role escalation (viewer → admin)                | High     |

---

## 🗂️ Project Structure

```
cloud-iam-abuse-detector/
├── data/
│   ├── simulated_logs.csv      # Sample demo logs
│   └── uploads/                # Runtime uploads (ignored in Git)
├── src/
│   ├── app.py                  # Flask web UI
│   ├── main.py                 # CLI entry point
│   ├── input_handler.py        # User input + validation
│   ├── detect_anomalies.py     # Detection rules engine
│   ├── reporter.py             # Alert summarization & evidence view
│   ├── simulate_events.py      # Log generator (demo only)
│   └── templates/
│       ├── index.html
│       └── results.html
├── README.md
└── requirements.txt
```

---

## 🚀 How It Works (High-Level Flow)

1. **Logs are generated or uploaded** (CSV)
2. **Detection rules analyze events**
3. **Suspicious activity is flagged**
4. **Alerts are summarized**
5. **Evidence is displayed (CLI / Web UI)**

---

## ▶️ Running the Project (CLI Mode)

### 1️⃣ Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2️⃣ (Optional) Generate Demo Logs

```bash
python src/simulate_events.py
```

This creates:

* `data/simulated_logs.csv`

---

### 3️⃣ Run Detection via CLI

```bash
python src/main.py
```

You will be prompted to enter the path to a CSV log file.

Example:

```
Enter path to IAM log CSV file:
data/simulated_logs.csv
```

---

## 🌐 Running the Web UI (Local)

Start the Flask app:

```bash
python src/app.py
```

Then open your browser:

```
http://127.0.0.1:5000
```

### Web UI Features

* Upload IAM log CSV
* Run detection rules
* View alert summary
* Inspect evidence linked to alerts

---

## 📊 Example Output

**Alert Summary**

```
Rule: Unusual Login Location (High-Risk Country)
Severity: High
Affected User: user_3
Evidence: Login from RU deviating from baseline (US)
```

Alerts are also saved locally for review.

---

## 🧪 Log Generator (Demo Only)

The `simulate_events.py` script allows users to:

* Generate realistic IAM logs
* Create repeatable demo scenarios
* Test detection logic safely

⚠️ Generated logs **do not represent real cloud provider formats**.

---

## 🛑 Limitations (By Design)

* Rule-based (no ML)
* Simplified log schema
* No real cloud API integration
* No persistence or authentication
* Local-only execution

These choices keep the focus on **detection logic and analyst reasoning**.

---

## 🎓 Who This Project Is For

* SOC Analysts
* Detection Engineers
* Cloud Security Learners
* Blue Team Students
* Security Interview Preparation

---

## 🧩 Future Enhancements (Optional)

* MITRE ATT&CK mapping per rule
* Timeline-based attack view
* More IAM abuse scenarios
* Cloud-native log formats
* Alert confidence scoring

---

## 🏷️ Tags

`cloud-security` · `iam` · `detection-engineering` · `soc` · `blue-team` · `cybersecurity-demo`

---

## 📌 Final Note

This project is intentionally **small, readable, and focused**.

It demonstrates **how security detections are designed**, not just how tools are used.
