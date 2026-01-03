from input_handler import load_log_file
from reporter import display_alerts_with_evidence
from detect_anomalies import run_all_detections
import pandas as pd

def main():
    print("=== Cloud IAM Abuse Detector ===")

    log_file_path = input("Enter path to IAM log CSV file: ").strip()

    try:
        df = load_log_file(log_file_path)
        print("[SUCCESS] Log file loaded successfully")
        print(f"Total events loaded: {len(df)}")

    except Exception as e:
        print(str(e))
        return

    print("\n[INFO] Running detection rules...")
    alerts = run_all_detections(df)

    if not alerts:
        print("[RESULT] No suspicious activity detected.")
        return

    alerts_df = pd.DataFrame(alerts)

    print("\n[ALERT SUMMARY]")
    print(alerts_df[["rule", "severity"]].value_counts())

    display_alerts_with_evidence(alerts, df)

    alerts_df.to_csv("data/alerts.csv", index=False)
    print("\n[SAVED] Alerts written to data/alerts.csv")

if __name__ == "__main__":
    main()
