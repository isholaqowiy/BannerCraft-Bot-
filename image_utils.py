import os
import httpx
from PIL import Image
from config import TEMP_DIR, PLATFORMS

def ensure_temp_directory():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

async def download_and_crop_banner(url: str, platform: str, user_id: int) -> str:
    """Downloads the generated raw image block and scales it precisely to platform spec ratios."""
    ensure_temp_directory()
    target_path = os.path.join(TEMP_DIR, f"banner_{user_id}.png")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            raw_img_path = os.path.join(TEMP_DIR, f"raw_{user_id}.png")
            with open(raw_img_path, "wb") as f:
                f.write(resp.content)
                
            dims = PLATFORMS.get(platform, {"width": 1200, "height": 400})
            with Image.open(raw_img_path) as img:
                # Dynamic aspect crop and thumbnail squeeze down layout pipeline operations
                img_resized = img.resize((dims["width"], dims["height"]), Image.Resampling.LANCZOS)
                img_resized.save(target_path, "PNG")
                
            if os.path.exists(raw_img_path): os.remove(raw_img_path)
            return target_path
    return None

def clean_user_files(user_id: int):
    if not os.path.exists(TEMP_DIR): return
    for filename in os.listdir(TEMP_DIR):
        if filename.startswith(f"banner_{user_id}") or filename.startswith(f"raw_{user_id}"):
            try: os.remove(os.path.join(TEMP_DIR, filename))
            except Exception: pass

