import os
import json
import time
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# --- PAGE CONFIG ---
st.set_page_config(page_title="NutriLens AR | Smart Glasses HUD", layout="wide")

# --- CUSTOM HUD STYLING ---
st.markdown("""
<style>
.hud-box {
    background: rgba(10, 25, 47, 0.88);
    border: 1px solid #00ffcc;
    border-radius: 12px;
    padding: 18px;
    color: #e6f1ff;
    font-family: 'Courier New', monospace;
    box-shadow: 0 0 18px rgba(0, 255, 204, 0.25);
    margin-bottom: 16px;
}
.hud-title {
    color: #00ffcc;
    font-size: 1.15rem;
    font-weight: bold;
    letter-spacing: 1.5px;
    border-bottom: 1px solid rgba(0, 255, 204, 0.3);
    padding-bottom: 6px;
    margin-bottom: 12px;
}
.hud-metric {
    font-size: 1.6rem;
    color: #00ffcc;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- STRUCTURED OUTPUT SCHEMA ---
class DishItem(BaseModel):
    name: str = Field(description="Name of the dish or food item (e.g., Masala Dosa, Sambar, Chicken Biryani)")
    portion_estimate: str = Field(description="Estimated serving size in grams or cups")
    calories: int = Field(description="Estimated calories in kcal")
    protein_g: int = Field(description="Protein in grams")
    carbs_g: int = Field(description="Carbohydrates in grams")
    fats_g: int = Field(description="Fats in grams")

class SmartGlassesHUDResponse(BaseModel):
    meal_detected: bool = Field(description="True if food/meal is present in the POV frame")
    meal_title: str = Field(description="Overall name of the meal platter")
    total_calories: int
    total_protein_g: int
    total_carbs_g: int
    total_fats_g: int
    items: list[DishItem]
    hud_status_badge: str = Field(description="Short 3-word badge: e.g., OPTIMAL PROTEIN FIT, CALORIE SURPLUS ALERT, BALANCED MACRO MEAL")
    voice_whisper: str = Field(description="1-2 sentence natural voice coaching message read aloud into the smart glasses bone-conduction audio")

# --- SIDEBAR: SMART GLASSES TELEMETRY & USER PROFILE ---
with st.sidebar:
    st.markdown("### 🕶️ NutriLens OS v2.6")
    st.caption("Connected: Gemini 3.8 Flash Live Edge Node")
    daily_target = st.slider("Daily Calorie Target (kcal)", 1500, 3500, 2850, step=50)
    consumed_so_far = st.number_input("Calories Consumed Today (kcal)", 0, 3500, 1450, step=50)
    protein_target = st.slider("Daily Protein Target (g)", 50, 220, 140, step=5)
    diet_focus = st.selectbox("Dietary Profile", [
        "South Indian High-Protein",
        "Balanced Athletic",
        "Calorie Deficit / Fat Loss",
        "Clean Bulk"
    ])
    enable_voice = st.toggle("🔊 Bone-Conduction Audio Whisper", value=True)
    remaining_cal = daily_target - consumed_so_far
    st.info(f"**Remaining Allowance:** {remaining_cal} kcal")

# --- HEADER ---
st.title("🕶️ NutriLens AR: Hands-Free Smart Glasses Nutrition Agent")
st.markdown(
    "**Zero-click meal logging.** Whenever your smart glasses detect a meal in your field of view, "
    "Gemini Vision automatically segments regional dishes, projects micro-HUD macros onto your lens, "
    "and whispers real-time portion adjustments."
)

col1, col2 = st.columns([1, 1.15])

with col1:
    st.subheader("📷 Smart Glasses POV Feed")
    input_mode = st.radio(
        "Select Optical Input Source:",
        ["Upload Meal Frame (Fast Demo)", "Live Optical Webcam Trigger"],
        horizontal=True
    )

    image_file = None
    if input_mode == "Upload Meal Frame (Fast Demo)":
        image_file = st.file_uploader("Simulate Smart Glasses Frame Capture", type=["jpg", "jpeg", "png", "webp"])
    else:
        image_file = st.camera_input("Blink or tap temple to capture POV")

    if image_file:
        img = Image.open(image_file)
        st.image(img, caption="POV Frame Captured [1080p Optical Sensor]", use_container_width=True)

with col2:
    st.subheader("⚡ Augmented Reality Lens Overlay (HUD)")
    if image_file:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Missing GEMINI_API_KEY environment variable. Set it in Cloud Run or locally.")
        else:
            with st.spinner("Gemini Vision analyzing POV frame & computing macro telemetry..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    You are NutriLens AR, an ambient AI nutrition agent running on smart glasses.
                    Analyze the first-person POV image.
                    User Profile: {diet_focus}.
                    Daily Calorie Target: {daily_target} kcal (Remaining today: {remaining_cal} kcal).
                    Daily Protein Target: {protein_target}g.
                    Pay special attention to regional Indian and Asian dishes (e.g., biryani, dosa, idli, sambar, Nei Sukka, curries, parotta) and hidden cooking oils/ghee.
                    Return accurate macro estimates and a concise, encouraging 1-2 sentence voice whisper telling the user how this plate fits their remaining {remaining_cal} kcal budget.
                    """
                    # Robust execution with automatic retry & fallback for high-traffic spikes (503/429)
                    candidate_models = ["gemini-3.8-flash", "gemini-2.5-flash-lite", "gemini-3.8-pro"]
                    response = None
                    used_model = None
                    last_err = None

                    for model_candidate in candidate_models:
                        for attempt in range(2):
                            try:
                                response = client.models.generate_content(
                                    model=model_candidate,
                                    contents=[img, prompt],
                                    config=types.GenerateContentConfig(
                                        response_mime_type="application/json",
                                        response_schema=SmartGlassesHUDResponse,
                                        temperature=0.2,
                                    ),
                                )
                                used_model = model_candidate
                                break
                            except Exception as e:
                                last_err = e
                                err_msg = str(e)
                                if "503" in err_msg or "UNAVAILABLE" in err_msg or "429" in err_msg:
                                    time.sleep(1.5)
                                    continue
                                break
                        if response:
                            break

                    if not response:
                        raise last_err

                    data = json.loads(response.text)

                    if not data.get("meal_detected", True):
                        st.warning("HUD Standby: No meal detected in current field of view.")
                    else:
                        new_remaining = remaining_cal - data["total_calories"]
                        # Render AR HUD Card
                        st.markdown(f"""
                        <div class="hud-box">
                            <div class="hud-title">● LIVE AR HUD // {data['hud_status_badge']}</div>
                            <h3 style="margin:0 0 8px 0; color:#fff;">{data['meal_title']}</h3>
                            <p style="margin:0; font-size:0.95rem; color:#8892b0;">
                                Post-Meal Calorie Balance: <b>{new_remaining} kcal</b> remaining today
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Plate Calories", f"{data['total_calories']} kcal")
                        m2.metric("Protein", f"{data['total_protein_g']} g")
                        m3.metric("Carbs", f"{data['total_carbs_g']} g")
                        m4.metric("Fats", f"{data['total_fats_g']} g")

                        st.markdown("#### 🔍 Optical Dish Segmentation")
                        st.dataframe(data["items"], use_container_width=True, hide_index=True)

                        st.markdown(f"""
                        <div class="hud-box" style="border-color:#64ffda;">
                            <div class="hud-title">🔊 BONE-CONDUCTION AUDIO WHISPER</div>
                            <i>"{data['voice_whisper']}"</i>
                        </div>
                        """, unsafe_allow_html=True)

                        if enable_voice:
                            clean_whisper = data["voice_whisper"].replace('"', '\\"').replace("'", "\\'")
                            components.html(f"""
                            <script>
                                window.speechSynthesis.cancel();
                                var msg = new SpeechSynthesisUtterance("{clean_whisper}");
                                msg.rate = 1.05;
                                window.speechSynthesis.speak(msg);
                            </script>
                            """, height=0)

                except Exception as e:
                    st.error(f"HUD Telemetry Error: {e}")
    else:
        st.markdown("""
        <div class="hud-box">
            <div class="hud-title">● HUD STANDBY // AWAITING GAZE LOCK</div>
            <p>Look at a meal plate or upload a sample POV frame on the left to trigger automatic Gemini Vision macro segmentation and audio coaching.</p>
        </div>
        """, unsafe_allow_html=True)
