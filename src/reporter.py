def display_alerts_with_evidence(alerts, df):
    print("\n=== DETAILED ALERT REPORT ===")

    for idx, alert in enumerate(alerts, start=1):
        print("\n" + "=" * 60)
        print(f"ALERT #{idx}")
        print(f"Rule     : {alert['rule']}")
        print(f"Severity : {alert['severity']}")
        print(f"User     : {alert['user_id']}")
        print(f"Time     : {alert['timestamp']}")
        print(f"Details  : {alert['details']}")

        print("\nEvidence Events:")
        print("-" * 60)

        evidence_df = df[df["event_id"].isin(alert["evidence_event_ids"])]
        print(
            evidence_df[
                ["event_id", "timestamp", "action", "ip_address", "location", "role"]
            ].to_string(index=False)
        )
