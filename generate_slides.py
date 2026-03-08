import os
import io
import time
from google import genai
from google.genai import types
from PIL import Image as PILImage

API_KEY = os.environ.get("gemini") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "슬라이드_이미지")
os.makedirs(OUTPUT_DIR, exist_ok=True)

slides = [
    {
        "filename": "01_히어로배너",
        "prompt": (
            "A photorealistic scene of an elderly Korean woman in her 80s, "
            "standing by a window with warm golden morning sunlight streaming in. "
            "A Korean national flag (Taegeukgi) is subtly visible through the window. "
            "She wears a traditional Korean hanbok or neat clothing, looking out peacefully. "
            "The mood is dignified, warm, and reverent. Shot with 50mm lens, soft natural lighting. "
            "No text, no watermarks, no logos, no words anywhere in the image."
        )
    },
    {
        "filename": "02_핵심혜택요약_배경",
        "prompt": (
            "A clean, minimal abstract background design in navy blue and white gradient. "
            "Soft circular shapes and gentle geometric patterns arranged in a 4-section grid layout. "
            "Government official document aesthetic. Modern Korean government design style. "
            "Subtle gold accent lines. Professional infographic background template. "
            "No text, no numbers, no words, no icons, purely abstract shapes and colors."
        )
    },
    {
        "filename": "03_신뢰지표_정부청사",
        "prompt": (
            "A photorealistic image of a modern Korean government building exterior "
            "(similar to Sejong Government Complex style). Clear blue sky with Korean national flags "
            "flying proudly. Wide-angle architectural photography. Clean, authoritative, trustworthy atmosphere. "
            "Spring season with cherry blossoms or green trees nearby. "
            "No text, no signage text, no words anywhere in the image."
        )
    },
    {
        "filename": "04_페인포인트_공감",
        "prompt": (
            "A photorealistic, emotionally moving scene of an elderly Korean woman in her 80s "
            "sitting alone in a small, modest traditional Korean room (ondol room). "
            "Seen from behind. Dim, muted lighting coming through a small window. "
            "The room is simple but clean - a small table, old family photo frame on the wall. "
            "Feeling of solitude, dignity in hardship, quiet resilience. Slightly desaturated, cool tones. "
            "No text, no words anywhere in the image."
        )
    },
    {
        "filename": "05_솔루션선언_희망",
        "prompt": (
            "A photorealistic image of beautiful Mugunghwa (Rose of Sharon, Korean national flower) "
            "blooming abundantly in a sunlit Korean garden. Bright warm sunlight breaking through, "
            "creating a dramatic transition from shadow to light. Symbolizing hope and new beginnings. "
            "Vibrant pink and white flowers against lush green foliage. Spring atmosphere. "
            "Shot with shallow depth of field, golden hour lighting. "
            "No text, no words anywhere in the image."
        )
    },
    {
        "filename": "06_혜택시각화",
        "prompt": (
            "A photorealistic overhead view of a clean, warm-toned wooden table. "
            "On it: a Korean bank passbook (통장), reading glasses, a small potted plant, "
            "and a warm cup of tea. Soft warm lighting from the side. "
            "Feeling of financial stability, simple daily happiness, comfort in old age. "
            "Cozy, reassuring atmosphere. Styled product photography aesthetic. "
            "No text, no numbers, no words anywhere in the image."
        )
    },
    {
        "filename": "07_자격확인_서류",
        "prompt": (
            "A photorealistic image of a neatly organized desk with official documents, "
            "a magnifying glass, a fountain pen, and a green checkmark stamp. "
            "Clean white desk surface, bright and orderly atmosphere. "
            "Suggesting document verification and eligibility checking process. "
            "Professional, organized, approachable feeling. Bright, clean tones. "
            "No text, no words, no readable content on documents."
        )
    },
    {
        "filename": "08_기존vs신규_비교",
        "prompt": (
            "A photorealistic conceptual image split in two halves. "
            "Left half: a closed wooden door in a dimly lit, cold-toned corridor. "
            "Right half: the same door wide open with warm, bright golden light flooding through. "
            "Dramatic contrast between darkness and light. Symbolizing change, improvement, "
            "new opportunity opening up. Cinematic lighting, architectural photography style. "
            "No text, no words anywhere in the image."
        )
    },
    {
        "filename": "09_신청절차_보훈청",
        "prompt": (
            "A photorealistic image of a bright, modern Korean public service center lobby. "
            "A friendly female staff member at a clean service counter, with comfortable waiting chairs. "
            "Warm, welcoming atmosphere with good lighting. Plants and Korean government decor. "
            "Suggesting an accessible, easy-to-visit government office. "
            "No people's faces in detail, showing the space and atmosphere more than individuals. "
            "No text, no signage text, no words anywhere in the image."
        )
    },
    {
        "filename": "10_희망과변화_가족",
        "prompt": (
            "A photorealistic image of an elderly Korean grandmother walking with her grandchild "
            "in a beautiful Korean park during spring. Cherry blossoms in full bloom. "
            "They are seen from behind, walking hand in hand on a peaceful path. "
            "Warm, golden afternoon sunlight filtering through the blossoms. "
            "Feeling of peace, family warmth, hopeful future, contentment. "
            "Soft bokeh background, 85mm lens aesthetic. "
            "No text, no words anywhere in the image."
        )
    },
]

for i, slide in enumerate(slides):
    print(f"\n[{i+1}/10] 생성 중: {slide['filename']}...")
    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=[slide["prompt"]],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="4:3",
                ),
            ),
        )

        saved = False
        for part in response.parts:
            if part.inline_data:
                raw_bytes = part.inline_data.data
                pil_img = PILImage.open(io.BytesIO(raw_bytes))
                filepath = os.path.join(OUTPUT_DIR, f"{slide['filename']}.png")
                pil_img.save(filepath, format="PNG")
                print(f"  -> 저장 완료: {filepath}")
                saved = True
                break
        if not saved:
            print(f"  -> 이미지 생성 실패 (응답에 이미지 없음)")

    except Exception as e:
        print(f"  -> 오류: {e}")

    if i < len(slides) - 1:
        time.sleep(3)

print("\n모든 이미지 생성 완료!")
