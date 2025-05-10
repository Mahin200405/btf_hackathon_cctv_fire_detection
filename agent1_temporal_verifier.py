import json
from collections import defaultdict

# === Load detection output from YOLO inference ===
with open("fire_detection_output.json", "r") as f:
    data = json.load(f)

# === Track detections across frames ===
# Structure: detections_by_label["fire"] = [{frame_id, area, confidence}, ...]
detections_by_label = defaultdict(list)

for frame in data:
    frame_id = frame["frame_id"]
    for det in frame["detections"]:
        label = det["label"]
        conf = det["confidence"]
        x, y, w, h = det["bbox"]
        area = w * h
        detections_by_label[label].append({
            "frame_id": frame_id,
            "confidence": conf,
            "area": area
        })

# === Filter and confirm persistent detections ===
confirmed_detections = []
MIN_FRAMES = 3             # must persist across this many frames
MIN_AREA = 1000            # box must be at least this large
MIN_CONFIDENCE = 0.15      # weak detections get filtered

for label, entries in detections_by_label.items():
    if len(entries) >= MIN_FRAMES:
        # Compute basic stats
        start = entries[0]["frame_id"]
        end = entries[-1]["frame_id"]
        duration = end - start + 1
        avg_area = sum(e["area"] for e in entries) / len(entries)
        max_conf = max(e["confidence"] for e in entries)

        if avg_area >= MIN_AREA and max_conf >= MIN_CONFIDENCE:
            confirmed_detections.append({
                "label": label,
                "start_frame": start,
                "end_frame": end,
                "duration_frames": duration,
                "average_area": round(avg_area, 2),
                "max_confidence": round(max_conf, 3),
                "status": "confirmed"
            })

# === Save verified results ===
with open("verified_detections.json", "w") as f:
    json.dump(confirmed_detections, f, indent=2)

print(f"✅ Agent 1: Verified {len(confirmed_detections)} persistent detections.")
