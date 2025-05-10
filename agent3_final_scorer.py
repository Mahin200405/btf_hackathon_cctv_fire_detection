import json

# === Load context-scored detections from Agent 2 ===
with open("context_scored_detections.json", "r") as f:
    detections = json.load(f)

# === Alert criteria rules
alert_rules = {
    "high": {"min_duration": 10, "min_score": 0.7},
    "moderate": {"min_duration": 20, "min_score": 0.5},
    "low": {"min_duration": 999, "min_score": 1.0}  # never trigger alert for low
}

# === Evaluate alert status
for det in detections:
    risk = det["risk_level"]
    rule = alert_rules[risk]

    duration = det["duration_frames"]
    score = det["context_score"]

    det["alert"] = duration >= rule["min_duration"] and score >= rule["min_score"]

# === Save final result
with open("final_alerts.json", "w") as f:
    json.dump(detections, f, indent=2)

# === Print summary
alerts = [d for d in detections if d["alert"]]
print(f"🚨 Agent 3: {len(alerts)} ALERT(S) triggered out of {len(detections)} detections.")
