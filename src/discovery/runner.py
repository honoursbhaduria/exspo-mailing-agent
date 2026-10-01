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

def run_discovery_cli(niche=DEFAULT_NICHE, limit=65):
    """
    Runs the discovery spider in a clean Python subprocess to avoid Twisted Reactor restart issues.
    """
    python_bin = sys.executable
    script_path = Path(__file__).resolve().parent / "_crawl_subprocess.py"
    
    cmd = [python_bin, str(script_path), "--niche", niche, "--limit", str(limit)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(RAW_DATA_PATH):
        df = pd.read_csv(RAW_DATA_PATH)
        return df
    else:
        raise RuntimeError(f"Discovery failed. Output: {result.stdout}\nErrors: {result.stderr}")

if __name__ == "__main__":
    print(f"Running micro-influencer discovery for {DEFAULT_NICHE}...")
    df = run_discovery_cli()
    print(f"Discovery complete! Discovered {len(df)} influencers. Saved to {RAW_DATA_PATH}")
    print(df[["name", "handle", "follower_count", "engagement_rate", "niche", "location"]].head(10))
