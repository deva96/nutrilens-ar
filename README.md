# NutriLens AR 🕶️🍽️
**Hands-Free Smart Glasses Nutrition & Macro Telemetry Agent powered by Gemini 3.8 Flash & Google Cloud Run.**

## Problem
Manual calorie counting apps fail because logging multi-item regional meals (such as South Indian platters, biryanis, or thalis) takes 3–5 minutes of tedious searching and guessing per meal. Furthermore, standard AI scanners hallucinate or misjudge ingredients without providing an interactive way for the user to calibrate or correct results.

## Solution
NutriLens AR eliminates manual logging and provides ambient, continuous optical intelligence. Built for optical smart glasses:
- **Spatial AR Segmentation**: Uses **Gemini 3.8 Flash Multimodal Vision** with 2D bounding box detection (`[ymin, xmin, ymax, xmax]`) to project glowing holographic HUD reticles directly over each dish on the lens.
- **Multimodal Feedback & AI Retry Loop**: If a dish or portion is misidentified, users can provide instant voice/text corrections (*"That's tofu, not paneer; and I only ate half the rice"*), triggering multi-turn AI re-evaluation.
- **Live In-Place Telemetry Editor**: Allows direct in-table micro-adjustments with instant recalculation of plate calories and macros.
- **Metabolic Sequence Coach (Biohack)**: Recommends the optimal sequence to consume items (e.g., fiber/vegetables and protein first) to blunt postprandial glucose spikes by up to 35%.
- **Persistent Glasses Memory**: Learns household cooking habits (e.g., low oil in sambar, black coffee without sugar) and injects them into future prompts.
- **Bone-Conduction Audio**: Speaks an actionable portion tip and real-time encouragement via web speech synthesis.

## Tech Stack
- **AI Model:** Google Gemini 3.8 Flash (`google-genai` SDK, Structured Outputs + Multimodal Vision)
- **Computer Vision:** Spatial AR Reticle Engine (PIL RGBA coordinate projection)
- **State Management:** Session-state telemetry caching with live pandas/data editor recalculation
- **Cloud Compute:** Google Cloud Run (Serverless Container)
- **Frontend Simulator:** Streamlit AR HUD Simulator + Web Speech Synthesis API

## Getting Started

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Gemini API key (or enter it directly in the sidebar):
   ```bash
   export GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
   ```

3. Launch the Streamlit HUD:
   ```bash
   streamlit run app.py
   ```

### Google Cloud Run Deployment
Deploy serverless container directly to Google Cloud Run:
```bash
gcloud run deploy nutrilens-ar \
  --source . \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
```
