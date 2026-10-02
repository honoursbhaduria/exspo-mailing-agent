import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import subprocess
import pandas as pd
from config.settings import RAW_DATA_PATH, DEFAULT_NICHE
from src.discovery.multi_platform_scraper import MultiPlatformInfluencerScraper
from src.discovery.playwright_scraper import PlaywrightInfluencerScraper


def run_discovery_cli(
    niche: str = DEFAULT_NICHE,
    limit: int = 65,
    engine: str = "scrapy",
    geo: str = "Global (All Regions)"
) -> pd.DataFrame:
    """
    Runs the multi-platform discovery pipeline across Collabstr UGC marketplace,
    YouTube channels, Instagram profiles, and verified creator directories.
    Appends newly discovered unique authentic influencers to the dataset on every execution,
    expanding the pool while preserving all existing curated and verified records.
    """
    print(f"Executing real multi-platform discovery for '{niche}' ({geo}) using {engine.upper()} engine...")

    # 1. Run MultiPlatformInfluencerScraper to harvest real creators across platforms
    scraper = MultiPlatformInfluencerScraper()
    discovered_creators = scraper.discover_creators(
        niche=niche,
        geo=geo,
        limit=limit,
        engine=engine
    )

    # 2. Run Playwright scraper if selected as engine
    if engine.lower() == "playwright":
        try:
            pw_scraper = PlaywrightInfluencerScraper(headless=True)
            pw_df = pw_scraper.scrape_niche(target_niche=niche, limit=limit)
            if not pw_df.empty:
                discovered_creators.extend(pw_df.to_dict(orient="records"))
        except Exception as e:
            print(f"Playwright discovery engine notice: {e}. Preserving live results...")

    # 3. Load active dataset (or seed fallback)
    base_dfs = []
    seed_path = RAW_DATA_PATH.parent / "influencers_seed.csv"
    if seed_path.exists():
        try:
            base_dfs.append(pd.read_csv(seed_path))
        except Exception:
            pass
    if RAW_DATA_PATH.exists():
        try:
            base_dfs.append(pd.read_csv(RAW_DATA_PATH))
        except Exception:
            pass

    current_df = pd.concat(base_dfs).drop_duplicates(subset=["handle"], keep="first") if base_dfs else pd.DataFrame()

    # 4. Merge discovered real creators with active dataset
    if discovered_creators:
        new_df = pd.DataFrame(discovered_creators)
        # Drop duplicates by handle
        combined_df = pd.concat([current_df, new_df]).drop_duplicates(subset=["handle"], keep="first")
        try:
            from src.database.db import upsert_many
            upsert_many(discovered_creators)
        except Exception as e:
            print(f"Database sync notice during discovery: {e}")
    else:
        combined_df = current_df

    combined_df.to_csv(RAW_DATA_PATH, index=False)
    print(f"Discovery pipeline: fetched {len(discovered_creators)} authentic influencers. Total dataset now: {len(combined_df)}")
    return combined_df


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--niche", default=DEFAULT_NICHE)
    parser.add_argument("--limit", default=65, type=int)
    parser.add_argument("--engine", default="scrapy", choices=["scrapy", "playwright"])
    parser.add_argument("--geo", default="Global (All Regions)")
    args = parser.parse_args()

    print(f"Running micro-influencer discovery for {args.niche} ({args.geo}) using {args.engine.upper()} engine...")
    df = run_discovery_cli(niche=args.niche, limit=args.limit, engine=args.engine, geo=args.geo)
    print(f"Discovery complete! Discovered {len(df)} influencers. Saved to {RAW_DATA_PATH}")
    print(df[["name", "handle", "follower_count", "engagement_rate", "niche", "location"]].tail(10))
