import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------
TOTAL_EVENTS = 1200
USERS = [f"user_{i}" for i in range(1, 21)]
LOCATIONS = ["US", "IN", "DE", "FR"]
HIGH_RISK_LOCATION = "RU"

ROLES = ["viewer", "editor", "admin"]

START_TIME = datetime.utcnow()

events = []

# -----------------------------
# Helper Functions
# -----------------------------
def random_timestamp(offset_minutes):
    return (START_TIME + timedelta(minutes=offset_minutes)).isoformat()

def generate_event(
    user,
    action,
    role,
    location,
    success=True,
    offset=0,
    resource="console"
):
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user,
        "timestamp": random_timestamp(offset),
        "action": action,
        "resource": resource,
        "role": role,
        "location": location,
        "success": success
    }

# -----------------------------
# 1. Normal Baseline Activity (≈80%)
# -----------------------------
current_minute = 0

for _ in range(range_count := int(TOTAL_EVENTS * 0.8)):
    user = random.choice(USERS)
    location = random.choice(LOCATIONS)
    events.append(
        generate_event(
            user=user,
            action="login",
            role="viewer",
            location=location,
            success=True,
            offset=current_minute
        )
    )
    current_minute += random.randint(1, 3)

# -----------------------------
# 2. Unusual Login Locations
# -----------------------------
for user in random.sample(USERS, 3):
    # Baseline login
    events.append(
        generate_event(
            user=user,
            action="login",
            role="viewer",
            location="US",
            offset=current_minute
        )
    )
    current_minute += 2

    # High-risk login
    events.append(
        generate_event(
            user=user,
            action="login",
            role="viewer",
            location=HIGH_RISK_LOCATION,
            offset=current_minute
        )
    )
    current_minute += 2

# -----------------------------
# 3. Brute Force Login Attempts
# -----------------------------
for user in random.sample(USERS, 3):
    for i in range(5):
        events.append(
            generate_event(
                user=user,
                action="login",
                role="viewer",
                location="US",
                success=False,
                offset=current_minute + i
            )
        )
    current_minute += 10

# -----------------------------
# 4. Rapid Privilege Escalation
# -----------------------------
for user in random.sample(USERS, 2):
    roles_sequence = ["viewer", "editor", "admin"]
    for i, role in enumerate(roles_sequence):
        events.append(
            generate_event(
                user=user,
                action="role_change",
                role=role,
                location="US",
                offset=current_minute + (i * 5),
                resource="iam"
            )
        )
    current_minute += 20

# -----------------------------
# Finalize Dataset
# -----------------------------
df = pd.DataFrame(events)
df = df.sort_values("timestamp")

df.to_csv("data/simulated_logs.csv", index=False)

print(f"[SUCCESS] Generated {len(df)} IAM log events")
print("[INFO] Dataset includes normal activity and simulated abuse patterns")
