from datetime import timedelta

# -----------------------------
# Configuration
# -----------------------------

HIGH_RISK_LOCATIONS = {"RU"}
ROLE_HIERARCHY = {
    "viewer": 1,
    "editor": 2,
    "admin": 3
}

FAILED_LOGIN_THRESHOLD = 3
FAILED_LOGIN_WINDOW = timedelta(minutes=10)

PRIV_ESCALATION_WINDOW = timedelta(minutes=30)

# -----------------------------
# Rule 1: Unusual Login Location (Baseline + High-Risk)
# -----------------------------

def detect_unusual_login_location(df):
    alerts = []
    user_baseline = {}

    login_events = df[df["action"] == "login"]

    for _, row in login_events.iterrows():
        user = row["user_id"]
        location = row["location"]

        # Establish baseline (first observed location)
        if user not in user_baseline:
            user_baseline[user] = location
            continue

        # Alert on deviation + high-risk country
        if location != user_baseline[user] and location in HIGH_RISK_LOCATIONS:
            alerts.append({
                "user_id": user,
                "rule": "Unusual Login Location (High-Risk Country)",
                "severity": "High",
                "timestamp": row["timestamp"],
                "details": f"Baseline={user_baseline[user]}, New={location}",
                "evidence_event_ids": [row["event_id"]]
            })

    return alerts

# -----------------------------
# Rule 2: Multiple Failed Login Attempts (Brute Force)
# -----------------------------

def detect_failed_logins(df):
    alerts = []

    failed_logins = df[
        (df["action"] == "login") &
        (df["success"] == False)
    ]

    for user, group in failed_logins.groupby("user_id"):
        group = group.sort_values("timestamp")
        timestamps = list(group["timestamp"])

        for i in range(len(timestamps)):
            window_start = timestamps[i]
            evidence_ids = [group.iloc[i]["event_id"]]

            for j in range(i + 1, len(timestamps)):
                if timestamps[j] - window_start <= FAILED_LOGIN_WINDOW:
                    evidence_ids.append(group.iloc[j]["event_id"])
                else:
                    break

            if len(evidence_ids) >= FAILED_LOGIN_THRESHOLD:
                alerts.append({
                    "user_id": user,
                    "rule": "Multiple Failed Login Attempts",
                    "severity": "High",
                    "timestamp": window_start,
                    "details": (
                        f"{len(evidence_ids)} failed logins within "
                        f"{FAILED_LOGIN_WINDOW}"
                    ),
                    "evidence_event_ids": evidence_ids
                })
                break

    return alerts

# -----------------------------
# Rule 3: Rapid Privilege Escalation
# -----------------------------

def detect_privilege_escalation(df):
    alerts = []

    role_changes = df[df["action"] == "role_change"]

    for user, group in role_changes.groupby("user_id"):
        group = group.sort_values("timestamp")

        previous_role = None
        previous_time = None
        previous_event_id = None

        for _, row in group.iterrows():
            current_role = row["role"]

            if previous_role:
                if ROLE_HIERARCHY[current_role] > ROLE_HIERARCHY[previous_role]:
                    time_diff = row["timestamp"] - previous_time

                    if time_diff <= PRIV_ESCALATION_WINDOW:
                        alerts.append({
                            "user_id": user,
                            "rule": "Rapid Privilege Escalation",
                            "severity": "High",
                            "timestamp": row["timestamp"],
                            "details": (
                                f"{previous_role} → {current_role} "
                                f"in {time_diff}"
                            ),
                            "evidence_event_ids": [
                                previous_event_id,
                                row["event_id"]
                            ]
                        })
                        break

            previous_role = current_role
            previous_time = row["timestamp"]
            previous_event_id = row["event_id"]

    return alerts

# -----------------------------
# Unified Detection Pipeline
# -----------------------------

def run_all_detections(df):
    alerts = []
    alerts.extend(detect_unusual_login_location(df))
    alerts.extend(detect_failed_logins(df))
    alerts.extend(detect_privilege_escalation(df))
    return alerts
