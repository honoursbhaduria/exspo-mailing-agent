import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import subprocess
import pandas as pd
from config.settings import RAW_DATA_PATH, DEFAULT_NICHE
from src.discovery.playwright_scraper import PlaywrightInfluencerScraper

def run_discovery_cli(niche=DEFAULT_NICHE, limit=65, engine="scrapy"):
    """
    Runs the discovery pipeline using either Scrapy or Playwright headless browser engine.
    If Scrapy fails or encounters network blocks, automatically falls back to Playwright.
    """
    if engine.lower() == "playwright":
        try:
            scraper = PlaywrightInfluencerScraper(headless=True)
            df = scraper.scrape_niche(target_niche=niche, limit=limit)
            if not df.empty:
                return df
        except Exception as e:
            print(f"Playwright discovery engine warning: {e}. Falling back to Scrapy/dataset...")

    python_bin = sys.executable
    script_path = Path(__file__).resolve().parent / "_crawl_subprocess.py"
    
    cmd = [python_bin, str(script_path), "--niche", niche, "--limit", str(limit)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(RAW_DATA_PATH):
        df = pd.read_csv(RAW_DATA_PATH)
        return df
    else:
        # Ultimate fallback to Playwright headless session
        scraper = PlaywrightInfluencerScraper(headless=True)
        return scraper.scrape_niche(target_niche=niche, limit=limit)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default=DEFAULT_NICHE)
    parser.add_argument("--limit", default=65, type=int)
    parser.add_argument("--engine", default="scrapy", choices=["scrapy", "playwright"])
    args = parser.parse_args()

    print(f"Running micro-influencer discovery for {args.niche} using {args.engine.upper()} engine...")
    df = run_discovery_cli(niche=args.niche, limit=args.limit, engine=args.engine)
    print(f"Discovery complete! Discovered {len(df)} influencers. Saved to {RAW_DATA_PATH}")
    print(df[["name", "handle", "follower_count", "engagement_rate", "niche", "location"]].head(10))
