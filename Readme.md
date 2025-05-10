# 🔥 Fire Detection & Alert System

This project uses a YOLOv11 model (trained on Roboflow) to detect fire or smoke from CCTV footage. It runs a multi-agent AI pipeline to verify, score, and trigger alerts.

## 🧠 Pipeline Stages

1. **YOLO Inference** (`object_detection.py`)
2. **Temporal Verification** (`agent1_temporal_verifier.py`)
3. **Scene Context Analysis** (`agent2_scene_context.py`)
4. **Threat Scoring & Alerting** (`agent3_final_scorer.py`)

## 🚀 How to Run

1. Clone this repo and `cd` into the folder
2. Create `.env` and add your Roboflow API key:
