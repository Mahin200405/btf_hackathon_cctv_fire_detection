import cv2
import json
import os
from datetime import timedelta
from dotenv import load_dotenv
from roboflow import Roboflow

# Load .env file and get API key
load_dotenv()
api_key = os.getenv("ROBOFLOW_API_KEY")

if not api_key:
    raise ValueError("❌ Roboflow API key not found in .env file!")

# Roboflow project/model setup
rf = Roboflow(api_key=api_key)
project = rf.workspace("btfhackathon12").project("fds-qgnwi-xpcn7")
model = project.version(1).model  

# Load video
cap = cv2.VideoCapture("fire_vids/fire2.mp4")  
frame_id = 0
fps = cap.get(cv2.CAP_PROP_FPS)
inference_interval = 5  # Run inference every 5 frames
output = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    timestamp = str(timedelta(seconds=frame_id / fps))

    if frame_id % inference_interval == 0:
        # Save frame temporarily
        frame_path = "temp_frame.jpg"
        cv2.imwrite(frame_path, frame)

        # Roboflow API call
        result = model.predict(frame_path, confidence=10, overlap=30).json()
        detections = []

        for pred in result["predictions"]:
            label = pred["class"]
            conf = round(pred["confidence"], 3)
            x = int(pred["x"] - pred["width"] / 2)
            y = int(pred["y"] - pred["height"] / 2)
            w = int(pred["width"])
            h = int(pred["height"])

            detections.append({
                "label": label,
                "confidence": conf,
                "bbox": [x, y, w, h]
            })

            # Draw bounding box on frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {conf}', (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        frame_data = {
            "frame_id": frame_id,
            "timestamp": timestamp,
            "detections": detections
        }
        output.append(frame_data)

    # Display frame
    cv2.imshow("Fire Detection - Roboflow", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frame_id += 1

cap.release()
cv2.destroyAllWindows()

# Save all detections to a file
with open("fire_detection_output.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Detection complete. Results saved to fire_detection_output.json")
