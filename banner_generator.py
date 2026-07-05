from openai import AsyncOpenAI
from config import OPENAI_API_KEY, PLATFORMS

async def generate_banner_url(data: dict) -> tuple:
    """Transforms structural user input data maps into a targeted descriptive prompt asset."""
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    
    platform_name = data.get("platform", "LinkedIn")
    dimensions = PLATFORMS.get(platform_name, {"width": 1024, "height": 1024})
    
    refined_prompt = (
        f"Professional social media banner design for a brand named '{data.get('brand')}', "
        f"featuring the tagline '{data.get('tagline', '')}'. Style description: {data.get('desc')}. "
        f"Visual aesthetic theme: {data.get('style', 'Modern Minimalism')}. Color palette directions: {data.get('colors', 'Harmonious')}. "
        f"Explicit composition rules: Optimized landscape layout framing structured exactly for a {platform_name} cover channel space. "
        f"Ensure empty copy spaces on outer bounds for profile avatars, high-end commercial branding graphic, perfect centered typography design asset execution."
    )
    
    try:
        # Utilizing fallback structural configurations for programmatic size matching constraints
        response = await client.images.generate(
            model="dall-e-3",
            prompt=refined_prompt,
            n=1,
            size="1024x1024" if platform_name == "Instagram" else "1792x1024",
            quality="hd"
        )
        return response.data[0].url, refined_prompt
    except Exception as e:
        print(f"OpenAI API Exception: {e}")
        return None, refined_prompt

