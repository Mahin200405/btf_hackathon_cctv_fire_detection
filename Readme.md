---

## 📚 Documentation

This section provides an in-depth overview of the tools, development process, and rationale behind the fire detection system.

### 🔧 Tools & Technologies Used

| Tool              | Purpose                                      |
|-------------------|----------------------------------------------|
| **Python 3.10+**   | Core language for the detection pipeline      |
| **YOLOv11 (Roboflow)** | Real-time object detection (fire/smoke)        |
| **Roboflow API**  | Hosted model inference & dataset management  |
| **OpenCV**        | Frame extraction and annotation              |
| **json**          | Storing and passing structured detection data |
| **dotenv**        | Securing API keys                            |
| **Git + GitHub**  | Version control and code sharing             |

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

