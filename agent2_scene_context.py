import json

# === Load verified detections from Agent 1 ===
with open("verified_detections.json", "r") as f:
    detections = json.load(f)

# === Hardcoded scene info (for now) ===
scene_context = {
    "camera_1": "office",
    "camera_2": "server_room",
    "camera_3": "kitchen"
}

scene_weights = {
    "office": 0.7,
    "server_room": 1.0,
    "kitchen": 0.3,
    "hallway": 0.4,
    "unknown": 0.5
}

# Time-based risk boost (optional)
def time_risk_boost(timestamp_str):
    # Placeholder: real implementation would extract time
    # Here we assume it's night (higher risk)
    return 1.2  # night-time boost

# === Analyze and enrich each detection ===
scored_detections = []

for det in detections:
    # For now, assume all came from "camera_1"
    camera_id = "camera_1"
    scene_type = scene_context.get(camera_id, "unknown")
    scene_weight = 1
    time_boost = time_risk_boost("00:00:00")  # placeholder time

    raw_score = det["max_confidence"] * scene_weight * time_boost
    raw_score = round(raw_score, 3)

    risk_level = (
        "high" if raw_score > 0.65 else
        "moderate" if raw_score > 0.4 else
        "low"
    )

    det.update({
        "scene_type": scene_type,
        "scene_risk_weight": scene_weight,
        "time_boost": time_boost,
        "context_score": raw_score,
        "risk_level": risk_level
    })

    scored_detections.append(det)

# === Save results ===
with open("context_scored_detections.json", "w") as f:
    json.dump(scored_detections, f, indent=2)

print(f"✅ Agent 2: Context scoring complete for {len(scored_detections)} detections.")
