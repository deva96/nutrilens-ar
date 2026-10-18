# NutriLens AR 🕶️🍽️
**Hands-Free Smart Glasses Nutrition & Macro Telemetry Agent powered by Gemini 3.8 Flash & Google Cloud Run.**

## Problem
Manual calorie counting apps fail because logging multi-item regional meals (such as South Indian platters, biryanis, or thalis) takes 3–5 minutes of tedious searching and guessing per meal.

## Solution
NutriLens AR eliminates manual logging. Built for optical smart glasses, it detects when a user looks down at a meal, uses **Gemini 3.8 Flash Multimodal Vision** with structured JSON outputs to segment every dish on the plate, projects a lightweight micro-HUD of calories and macros onto the lens, and speaks a 2-second actionable portion tip via bone-conduction audio.

## Tech Stack
- **AI Model:** Google Gemini 3.8 Flash (`google-genai` SDK, Structured Outputs + Multimodal Vision)
- **Cloud Compute:** Google Cloud Run (Serverless Container)
- **Frontend Simulator:** Streamlit AR HUD Simulator + Web Speech Synthesis API

## Getting Started

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your Gemini API key:
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
