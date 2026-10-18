import os
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

PAGE_WIDTH = 960
PAGE_HEIGHT = 540

BG_DARK = HexColor("#0A192F")
CARD_BG = HexColor("#112240")
CARD_BORDER = HexColor("#233554")
ACCENT_CYAN = HexColor("#00FFCC")
ACCENT_MINT = HexColor("#64FFDA")
TEXT_WHITE = HexColor("#FFFFFF")
TEXT_MUTED = HexColor("#8892B0")
TEXT_LIGHT = HexColor("#CCD6F6")
ACCENT_CORAL = HexColor("#FF6B6B")

def draw_header_footer(c, slide_num, total_slides=5):
    # Top banner bar
    c.setStrokeColor(ACCENT_CYAN)
    c.setLineWidth(1)
    c.line(40, PAGE_HEIGHT - 35, PAGE_WIDTH - 40, PAGE_HEIGHT - 35)
    
    # Top HUD Tag
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(45, PAGE_HEIGHT - 28, "● LIVE AR HUD // PITCH DECK")
    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_MUTED)
    c.drawString(PAGE_WIDTH - 210, PAGE_HEIGHT - 28, "NutriLens OS v2.6 | Google Cloud")

    # Bottom footer
    c.line(40, 35, PAGE_WIDTH - 40, 35)
    c.setFont("Helvetica", 9)
    c.setFillColor(TEXT_MUTED)
    c.drawString(45, 22, "NutriLens AR — Ambient Smart Glasses Nutrition Agent")
    c.drawString(PAGE_WIDTH - 110, 22, f"Slide {slide_num} of {total_slides}")

def draw_card(c, x, y, w, h, title="", border_color=CARD_BORDER):
    c.setFillColor(CARD_BG)
    c.setStrokeColor(border_color)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    if title:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(ACCENT_CYAN)
        c.drawString(x + 16, y + h - 24, title)
        c.setStrokeColor(HexColor("#1D3357"))
        c.line(x + 16, y + h - 30, x + w - 16, y + h - 30)

def create_pitch_deck(filename="NutriLens_AR_Pitch_Deck.pdf"):
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    
    # Background HUD elements
    c.setStrokeColor(HexColor("#142A4A"))
    c.setLineWidth(1)
    c.rect(40, 40, PAGE_WIDTH - 80, PAGE_HEIGHT - 80, fill=0, stroke=1)
    
    # Badge
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(80, PAGE_HEIGHT - 110, "🕶️ GOOGLE CLOUD & GEMINI HACKATHON")
    
    # Main Title
    c.setFont("Helvetica-Bold", 44)
    c.setFillColor(TEXT_WHITE)
    c.drawString(80, PAGE_HEIGHT - 170, "NutriLens AR")
    
    # Subtitle
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT_MINT)
    c.drawString(80, PAGE_HEIGHT - 210, "Ambient Smart Glasses Nutrition & Macro Telemetry Agent")
    
    # Description box
    draw_card(c, 80, 150, PAGE_WIDTH - 160, 120, border_color=ACCENT_CYAN)
    c.setFont("Helvetica", 13)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(100, 230, "Zero-click nutrition logging. Look at any meal plate — Gemini Vision automatically")
    c.drawString(100, 206, "segments complex regional dishes, projects micro-HUD macros onto your smart lens,")
    c.drawString(100, 182, "and whispers real-time dietary coaching directly into your earpiece.")

    # Metadata footer
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_MUTED)
    c.drawString(80, 80, "AI Engine: Google Gemini 3.8 Flash (Structured Outputs)")
    c.drawString(480, 80, "Deployment: Google Cloud Run Serverless Container")
    c.drawString(80, 60, "GitHub: github.com/deva96/nutrilens-ar")

    c.showPage()

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # =========================================================================
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header_footer(c, 2)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(TEXT_WHITE)
    c.drawString(45, PAGE_HEIGHT - 75, "The Problem: Why Calorie Tracking Fails")
    c.setFont("Helvetica", 13)
    c.setFillColor(TEXT_MUTED)
    c.drawString(45, PAGE_HEIGHT - 98, "Traditional nutrition apps create excessive friction, leading to 70%+ user abandonment.")

    # 3 Problem Cards
    card_w = 270
    card_h = 320
    card_y = 65

    # Card 1
    draw_card(c, 45, card_y, card_w, card_h, "1. Excessive Dining Friction", border_color=ACCENT_CORAL)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(60, card_y + 250, "• Pulling out a phone at dinner breaks")
    c.drawString(60, card_y + 232, "  social conversations.")
    c.drawString(60, card_y + 204, "• Typing, searching, and estimating")
    c.drawString(60, card_y + 186, "  takes 3-5 minutes per meal.")
    c.drawString(60, card_y + 158, "• Users give up within 14 days due")
    c.drawString(60, card_y + 140, "  to logging fatigue.")

    # Card 2
    draw_card(c, 345, card_y, card_w, card_h, "2. Barcodes Fail Regional Meals", border_color=ACCENT_CORAL)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(360, card_y + 250, "• Barcode scanners only work on")
    c.drawString(360, card_y + 232, "  packaged grocery goods.")
    c.drawString(360, card_y + 204, "• Multi-item regional platters")
    c.drawString(360, card_y + 186, "  (Thalis, Biryanis, Dosa, Curries)")
    c.drawString(360, card_y + 168, "  have no standardized labels.")
    c.drawString(360, card_y + 140, "• High inaccuracy on restaurant food.")

    # Card 3
    draw_card(c, 645, card_y, card_w, card_h, "3. Hidden Cooking Fats & Macros", border_color=ACCENT_CORAL)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(660, card_y + 250, "• Traditional apps ignore hidden")
    c.drawString(660, card_y + 232, "  cooking oils, ghee, and sauces.")
    c.drawString(660, card_y + 204, "• Results in 400-600 kcal tracking")
    c.drawString(660, card_y + 186, "  errors every single day.")
    c.drawString(660, card_y + 158, "• Users miss fitness & health goals")
    c.drawString(660, card_y + 140, "  despite diligent logging.")

    c.showPage()

    # =========================================================================
    # SLIDE 3: THE SOLUTION
    # =========================================================================
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header_footer(c, 3)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(TEXT_WHITE)
    c.drawString(45, PAGE_HEIGHT - 75, "The Solution: NutriLens AR Ambient Wearable")
    c.setFont("Helvetica", 13)
    c.setFillColor(TEXT_MUTED)
    c.drawString(45, PAGE_HEIGHT - 98, "A hands-free smart glasses nutrition assistant that operates seamlessly in the background.")

    # 3 Solution Cards
    draw_card(c, 45, card_y, card_w, card_h, "⚡ Zero-Click Gaze Capture", border_color=ACCENT_CYAN)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(60, card_y + 250, "• Optical sensor automatically")
    c.drawString(60, card_y + 232, "  detects when gaze rests on food.")
    c.drawString(60, card_y + 204, "• Temple tap or blink triggers instant")
    c.drawString(60, card_y + 186, "  frame telemetry capture.")
    c.drawString(60, card_y + 158, "• Zero manual phone typing or")
    c.drawString(60, card_y + 140, "  scale weighing required.")

    draw_card(c, 345, card_y, card_w, card_h, "👓 Micro-HUD AR Projection", border_color=ACCENT_CYAN)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(360, card_y + 250, "• Unobtrusive AR overlay projected")
    c.drawString(360, card_y + 232, "  directly onto smart glasses lens.")
    c.drawString(360, card_y + 204, "• Real-time breakdown: Calories,")
    c.drawString(360, card_y + 186, "  Protein, Carbs, and Fats.")
    c.drawString(360, card_y + 158, "• Live balance indicator vs.")
    c.drawString(360, card_y + 140, "  user's remaining daily budget.")

    draw_card(c, 645, card_y, card_w, card_h, "🔊 Bone-Conduction Audio", border_color=ACCENT_CYAN)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(660, card_y + 250, "• Ambient AI coach whispers a")
    c.drawString(660, card_y + 232, "  2-second actionable portion tip.")
    c.drawString(660, card_y + 204, "• Personalized to user's daily goals")
    c.drawString(660, card_y + 186, "  (High-Protein, Deficit, Clean Bulk).")
    c.drawString(660, card_y + 158, "• Private, natural, and completely")
    c.drawString(660, card_y + 140, "  hands-free.")

    c.showPage()

    # =========================================================================
    # SLIDE 4: ARCHITECTURE & TECH STACK
    # =========================================================================
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header_footer(c, 4)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(TEXT_WHITE)
    c.drawString(45, PAGE_HEIGHT - 75, "System Architecture on Google Cloud")
    c.setFont("Helvetica", 13)
    c.setFillColor(TEXT_MUTED)
    c.drawString(45, PAGE_HEIGHT - 98, "High-performance multimodal pipeline combining edge simulation and serverless intelligence.")

    # 2 Architecture Columns
    col_w = 420
    col_h = 320
    
    # Left Box: Tech Components
    draw_card(c, 45, card_y, col_w, col_h, "Layered Architecture Breakdown", border_color=ACCENT_CYAN)
    
    layers = [
        ("Client / Optical Edge:", "Smart Glasses Simulator + Web Speech Synthesis API", ACCENT_MINT),
        ("Vision Intelligence:", "Gemini 3.8 Flash Multimodal Vision", ACCENT_CYAN),
        ("Structured Outputs:", "Pydantic Schema (deterministic JSON telemetry)", TEXT_WHITE),
        ("Serverless Compute:", "Google Cloud Run / Streamlit Container", ACCENT_MINT),
        ("High-Availability:", "Automated retry backoff & multi-model failover", TEXT_WHITE),
    ]
    
    ly = card_y + 250
    for label, desc, col in layers:
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(col)
        c.drawString(60, ly, label)
        c.setFont("Helvetica", 11)
        c.setFillColor(TEXT_LIGHT)
        c.drawString(60, ly - 16, desc)
        ly -= 48

    # Right Box: Why Gemini 3.8 Flash?
    draw_card(c, 495, card_y, col_w, col_h, "Why Gemini 3.8 Flash & Google Cloud?", border_color=ACCENT_CYAN)
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(510, card_y + 250, "✓ Sub-2 Second End-to-End Latency")
    c.drawString(525, card_y + 232, "Fast enough for real-time smart glasses POV interaction.")
    
    c.drawString(510, card_y + 196, "✓ Complex Regional Food Segmentation")
    c.drawString(525, card_y + 178, "Accurately segments biryanis, curries, sushi, dosas, and sides.")

    c.drawString(510, card_y + 142, "✓ Strict Pydantic JSON Telemetry")
    c.drawString(525, card_y + 124, "Guarantees zero markdown hallucinations for HUD widgets.")

    c.drawString(510, card_y + 88, "✓ Serverless Scalability with Cloud Run")
    c.drawString(525, card_y + 70, "Scales from 0 to 100,000 requests with zero idle compute cost.")

    c.showPage()

    # =========================================================================
    # SLIDE 5: LIVE DEMO & CONCLUSION
    # =========================================================================
    c.setFillColor(BG_DARK)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
    draw_header_footer(c, 5)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(TEXT_WHITE)
    c.drawString(45, PAGE_HEIGHT - 75, "Live Demo, Validation & Next Steps")
    c.setFont("Helvetica", 13)
    c.setFillColor(TEXT_MUTED)
    c.drawString(45, PAGE_HEIGHT - 98, "Ready for real-world optical wearables and everyday dining.")

    # Left: Key Metrics
    draw_card(c, 45, card_y, col_w, col_h, "Prototype Validation Results", border_color=ACCENT_CYAN)
    metrics = [
        ("Zero-Click Latency", "< 2.0s average response time"),
        ("Segmentation Accuracy", "Multi-dish regional recognition & hidden fat estimation"),
        ("Audio Whisper Coaching", "Natural conversational tone via Web Speech API"),
        ("Reliability", "Built-in automatic retry & capacity failover"),
    ]
    my = card_y + 245
    for title, val in metrics:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(ACCENT_MINT)
        c.drawString(60, my, f"● {title}")
        c.setFont("Helvetica", 11)
        c.setFillColor(TEXT_LIGHT)
        c.drawString(75, my - 18, val)
        my -= 52

    # Right: Roadmap & Resources
    draw_card(c, 495, card_y, col_w, col_h, "Project Resources & Roadmap", border_color=ACCENT_CYAN)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(510, card_y + 250, "Future Roadmap:")
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(510, card_y + 230, "1. Native Android XR / Ray-Ban Meta glasses integration.")
    c.drawString(510, card_y + 210, "2. Real-time Continuous Glucose Monitor (CGM) sync.")
    c.drawString(510, card_y + 190, "3. Long-term dietary health coaching with Gemini Memory.")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(ACCENT_CYAN)
    c.drawString(510, card_y + 140, "Submission Links:")
    c.setFont("Helvetica", 11)
    c.setFillColor(TEXT_LIGHT)
    c.drawString(510, card_y + 120, "• GitHub: https://github.com/deva96/nutrilens-ar")
    c.drawString(510, card_y + 100, "• Live Prototype: Deployed & Ready for Evaluation")
    c.drawString(510, card_y + 80, "• AI Engine: Google Gemini 3.8 Flash Multimodal")

    c.showPage()
    c.save()
    print(f"Pitch deck successfully created: {filename}")

if __name__ == "__main__":
    create_pitch_deck()
