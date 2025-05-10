---

## 📚 Documentation

This section provides an in-depth overview of the tools, development process, and rationale behind the fire detection system.

### 🔧 Tools & Technologies Used

- **Python 3.10+**  
  Core language used for developing the entire pipeline.

- **YOLOv11 (via Roboflow)**  
  Deep learning object detection model for identifying fire and smoke in video frames.

- **Roboflow API**  
  Used for hosting the trained model and running inference on video frames.

- **OpenCV**  
  Handles video capture, frame-by-frame processing, and visual annotation with bounding boxes.

- **json module**  
  Used to structure, store, and transfer detection data between agents.

- **python-dotenv**  
  Secures API keys and loads environment variables from a `.env` file.

- **Git & GitHub**  
  For version control, team collaboration, and hosting the project source code.

---

### 🧠 Development Pipeline

The solution is designed as a modular AI pipeline:

1. **📦 Object Detection (`object_detection.py`)**
   - Uses a custom YOLOv11 model trained on fire/smoke datasets via Roboflow.
   - Frames are extracted from video, passed to the Roboflow API, and detections are saved to `fire_detection_output.json`.

2. **🔁 Agent 1: Temporal Verifier**
   - Verifies if fire/smoke persists over time.
   - Filters out one-frame false positives and stores confirmed detections.

3. **🔍 Agent 2: Scene Context Analyzer**
   - Assigns scene types like `"office"`, `"server_room"`, etc.
   - Adds risk weights and applies a time-based threat boost.
   - Computes a context-aware threat score.

4. **🚨 Agent 3: Threat Scorer**
   - Applies final scoring logic.
   - Triggers alerts only if detection is long-lasting, confident, and contextually risky.
   - Final output is stored in `final_alerts.json`.

---

### 💡 Thought Process

- **Why CCTV?**  
  Smoke detectors often respond late — visible smoke or sparks are observable sooner via cameras already deployed in offices.

- **Why a Multi-Agent Pipeline?**  
  Fire detection is error-prone. A series of light AI agents ensures:
  - Fewer false positives
  - Scalable context-awareness
  - Edge deployability

- **Why Roboflow?**  
  Roboflow lets us train + deploy vision models easily, saving time and allowing us to focus on pipeline design.

---

