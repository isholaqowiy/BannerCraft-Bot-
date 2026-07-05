import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TEMP_DIR = "temp_banners"
DB_NAME = "bannercraft.db"

# Platform Dimensions Registry
PLATFORMS = {
    "YouTube": {"width": 2560, "height": 1440, "aspect": "16:9"},
    "LinkedIn": {"width": 1584, "height": 396, "aspect": "4:1"},
    "X (Twitter)": {"width": 1500, "height": 500, "aspect": "3:1"},
    "Facebook": {"width": 820, "height": 312, "aspect": "16:9"}
}

