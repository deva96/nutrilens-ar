import json
import os
from PIL import Image
from pydantic import BaseModel, Field

# Import schema and helper functions directly
from app import DishItem, SmartGlassesHUDResponse, draw_ar_hud_overlay, load_user_memory, save_user_memory

def run_tests():
    print("Starting tests...")
    
    # 1. Test DishItem and SmartGlassesHUDResponse schemas
    item1 = DishItem(
        name="Masala Dosa",
        portion_estimate="1 piece (180g)",
        calories=280,
        protein_g=6,
        carbs_g=42,
        fats_g=10,
        confidence_score=0.96,
        box_2d=[120, 150, 480, 850]
    )
    item2 = DishItem(
        name="Sambar",
        portion_estimate="1 bowl (150ml)",
        calories=85,
        protein_g=4,
        carbs_g=14,
        fats_g=2,
        confidence_score=0.91,
        box_2d=[520, 200, 780, 420]
    )
    
    hud_resp = SmartGlassesHUDResponse(
        meal_detected=True,
        meal_title="South Indian Dosa & Sambar Platter",
        total_calories=365,
        total_protein_g=10,
        total_carbs_g=56,
        total_fats_g=12,
        items=[item1, item2],
        hud_status_badge="BALANCED MACRO FIT",
        voice_whisper="Balanced choice. Consider consuming the sambar first to blunt blood sugar response.",
        eating_sequence_guide="Consume the fiber-rich sambar first before the dosa crepe to slow gastric emptying.",
        potential_ambiguities=["Ghee content on dosa crust"]
    )
    
    serialized = hud_resp.model_dump_json()
    assert len(serialized) > 50
    reloaded = SmartGlassesHUDResponse.model_validate_json(serialized)
    assert reloaded.total_calories == 365
    assert len(reloaded.items) == 2
    print("✓ Schema serialization and validation passed.")

    # 2. Test AR Overlay Drawing
    sample_path = os.path.join(os.path.dirname(__file__), "sample_meal.jpg")
    if os.path.exists(sample_path):
        base_img = Image.open(sample_path)
    else:
        base_img = Image.new("RGB", (800, 600), (20, 30, 40))
        
    ar_overlay = draw_ar_hud_overlay(base_img, [item1.model_dump(), item2.model_dump()])
    assert ar_overlay.size == base_img.size
    print(f"✓ AR HUD overlay rendered successfully: dimensions {ar_overlay.size}.")

    # 3. Test Memory Persistence
    initial_mem = load_user_memory()
    assert isinstance(initial_mem, list)
    test_rule = "Test rule: always prefer black coffee"
    save_user_memory(initial_mem + [test_rule])
    loaded_mem = load_user_memory()
    assert test_rule in loaded_mem
    # Clean up test rule
    save_user_memory(initial_mem)
    print("✓ Smart glasses memory profile persistence verified.")

    print("\nALL UNIT TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
