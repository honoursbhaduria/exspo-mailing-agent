import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"
LOGO_PATH = IMAGES_DIR / "logo.png"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Default File Paths
RAW_DATA_PATH = DATA_DIR / "influencers_raw.csv"
PROCESSED_DATA_PATH = DATA_DIR / "influencers_processed.csv"
OUTREACH_LOG_PATH = DATA_DIR / "outreach_log.csv"

# Influencer Filtering Thresholds (Micro-influencers definition)
MIN_FOLLOWERS = int(os.getenv("MIN_FOLLOWERS", 5000))
MAX_FOLLOWERS = int(os.getenv("MAX_FOLLOWERS", 100000))
MIN_ENGAGEMENT_RATE = float(os.getenv("MIN_ENGAGEMENT_RATE", 2.0)) # 2.0%

# Target Niche Options
DEFAULT_NICHE = os.getenv("DEFAULT_NICHE", "Fashion & Beauty")
AVAILABLE_NICHES = [
    "Fashion & Beauty",
    "Technology & AI",
    "Fitness & Wellness",
    "Lifestyle & Travel",
    "Fintech & Crypto"
]

# APIs & Credentials
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "onboarding@resend.dev")
SIMULATION_MODE = os.getenv("SIMULATION_MODE", "True").lower() in ("true", "1", "yes")
