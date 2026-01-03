import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------
NUM_EVENTS = 300
START_TIME = datetime.now() - timedelta(days=7)

# Users and their normal properties
USERS = {
    "user_1": {"home_location": "US", "role": "viewer"},
    "user_2": {"home_location": "US", "role": "editor"},
    "user_3": {"home_location": "UK", "role": "viewer"},  # compromised user
    "user_4": {"home_location": "DE", "role": "editor"},
    "user_5": {"home_location": "US", "role": "viewer"},
}

ROLE_HIERARCHY = ["viewer", "editor", "admin"]

RESOURCES = ["s3_bucket", "db_server", "config_file"]

IP_POOLS = {
    "US": ["34.12.45.1", "34.12.45.2"],
    "UK": ["51.140.10.1", "51.140.10.2"],
    "DE": ["18.196.5.1", "18.196.5.2"],
    "RU": ["185.220.101.1"]  # attacker IP
}

# Attack configuration
COMPROMISED_USER = "user_3"
ATTACK_LOCATION = "RU"
ATTACK_START = START_TIME + timedelta(days=6)

events = []

# Track current role per user (stateful, realistic)
current_roles = {u: USERS[u]["role"] for u in USERS}

# -----------------------------
# Event Generation
# -----------------------------
for i in range(NUM_EVENTS):
    user = random.choice(list(USERS.keys()))
    action = random.choices(
        ["login", "resource_access", "role_change"],
        weights=[0.5, 0.35, 0.15]
    )[0]

    success = True
    location = USERS[user]["home_location"]
    ip = random.choice(IP_POOLS[location])
    role = current_roles[user]

    # -----------------------------
    # NORMAL BEHAVIOR
    # -----------------------------
    timestamp = START_TIME + timedelta(
        minutes=random.randint(0, 7 * 24 * 60)
    )

    # -----------------------------
    # ATTACK BEHAVIOR (user_3)
    # -----------------------------
    if user == COMPROMISED_USER and random.random() < 0.25:
        location = ATTACK_LOCATION
        ip = IP_POOLS["RU"][0]

        # Brute-force login attack
        if action == "login":
            success = False
            timestamp = ATTACK_START + timedelta(
                minutes=random.randint(0, 8)
            )

        # Rapid privilege escalation
        if action == "role_change":
            current_index = ROLE_HIERARCHY.index(current_roles[user])
            if current_index < len(ROLE_HIERARCHY) - 1:
                role = ROLE_HIERARCHY[current_index + 1]
                current_roles[user] = role
                timestamp = ATTACK_START + timedelta(
                    minutes=random.randint(10, 30)
                )

    # -----------------------------
    # Normal role changes (slow, rare)
    # -----------------------------
    if action == "role_change" and user != COMPROMISED_USER:
        if random.random() < 0.05:
            current_index = ROLE_HIERARCHY.index(current_roles[user])
            if current_index < len(ROLE_HIERARCHY) - 1:
                role = ROLE_HIERARCHY[current_index + 1]
                current_roles[user] = role

    event = {
        "event_id": i + 1,
        "user_id": user,
        "timestamp": timestamp,
        "action": action,
        "success": success,
        "role": role,
        "resource": random.choice(RESOURCES),
        "ip_address": ip,
        "location": location
    }

    events.append(event)

# -----------------------------
# Save Logs
# -----------------------------
df = pd.DataFrame(events).sort_values("timestamp")
df.to_csv("data/simulated_logs.csv", index=False)

print("Realistic simulated IAM logs saved to data/simulated_logs.csv")
