import pandas as pd
import os

REQUIRED_COLUMNS = {
    "event_id",
    "user_id",
    "timestamp",
    "action",
    "resource",
    "role",
    "ip_address",
    "location",
    "success"
}

def load_log_file(file_path: str) -> pd.DataFrame:
    # 1. Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[ERROR] File not found: {file_path}")

    # 2. Check file extension
    if not file_path.lower().endswith(".csv"):
        raise ValueError("[ERROR] Only CSV files are supported")

    # 3. Load CSV
    df = pd.read_csv(file_path)

    # 4. Validate columns
    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(
            f"[ERROR] Missing required columns: {missing_cols}"
        )

    # 5. Parse timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if df["timestamp"].isnull().any():
        raise ValueError("[ERROR] Invalid timestamp format detected")

    return df
