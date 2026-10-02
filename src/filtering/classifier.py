import re
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from typing import Dict, Any, Tuple, Optional
from config.settings import (
    MIN_FOLLOWERS,
    MAX_FOLLOWERS,
    MIN_ENGAGEMENT_RATE,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH
)

class InfluencerClassifier:
    """
    Evaluates influencer profiles against quantitative and qualitative criteria
    to qualify or disqualify them for brand collaboration outreach:
    - Follower count bounds (Micro-influencer scale: 5,000 - 100,000)
    - Minimum engagement rate threshold (e.g. >= 2.0%)
    - Category / Niche & Brand-fit semantic alignment
    - Audience Geography matching (220+ countries / ISO codes or Global)
    - Social Media Platform matching (Instagram, TikTok, YouTube, or All)
    """
    def __init__(
        self,
        min_followers: int = MIN_FOLLOWERS,
        max_followers: int = MAX_FOLLOWERS,
        min_engagement: float = MIN_ENGAGEMENT_RATE,
        target_niche: str = "Fashion & Beauty",
        target_geography: str = "Global (All Regions)",
        target_platform: str = "All Platforms"
    ):
        self.min_followers = min_followers
        self.max_followers = max_followers
        self.min_engagement = min_engagement
        self.target_niche = target_niche
        self.target_geography = target_geography or "Global (All Regions)"
        self.target_platform = target_platform or "All Platforms"

    @classmethod
    def from_yaml(cls, config_path: str = "config/filtering.yaml") -> "InfluencerClassifier":
        """
        Instantiates classifier using declarative parameters from config/filtering.yaml.
        """
        try:
            import yaml
            from pathlib import Path
            p = Path(config_path)
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
                followers_cfg = cfg.get("followers", {})
                return cls(
                    min_followers=followers_cfg.get("min", MIN_FOLLOWERS),
                    max_followers=followers_cfg.get("max", MAX_FOLLOWERS),
                    min_engagement=float(cfg.get("engagement_rate", {}).get("min", MIN_ENGAGEMENT_RATE)),
                    target_niche=cfg.get("niche", "Fashion & Beauty"),
                    target_geography=cfg.get("geography", "Global (All Regions)"),
                    target_platform=cfg.get("platform", "All Platforms")
                )
        except Exception:
            pass
        return cls()

    def _matches_geography(self, geo_str: str, loc_str: str) -> bool:
        """
        Checks whether creator's audience geography or location matches the target country.
        Supports full country names (e.g. 'United States'), ISO codes ('US'), and aliases.
        """
        if not self.target_geography or any(
            g in self.target_geography.lower() 
            for g in ["global", "all regions", "all countries", "worldwide"]
        ):
            return True

        target = self.target_geography.strip()
        combined = f"{geo_str} {loc_str}".lower()

        # Extract ISO code if enclosed in parentheses (e.g. "US" from "United States (US)")
        iso_code = ""
        country_name = target.lower()
        if "(" in target and ")" in target:
            iso_code = target[target.find("(") + 1 : target.find(")")].strip().lower()
            country_name = target[: target.find("(")].strip().lower()

        # 1. Known country aliases & specific disambiguations
        if iso_code == "ca" or "canada" in country_name:
            if any(term in combined for term in [", ca", "canada", "toronto", "ontario", "vancouver", "edmonton", "calgary", "montreal"]):
                if not any(u in combined for u in [", us", "united states", "usa"]):
                    return True
            return False

        if iso_code == "gb" or "united kingdom" in country_name or "britain" in country_name:
            if any(term in combined for term in ["gb", "uk", "united kingdom", "london", "england", "scotland", "wales", "brc", "ess", "man"]):
                return True
        elif iso_code == "us" or "united states" in country_name or "america" in country_name:
            if any(term in combined for term in [", us", " usa", "united states", "fl, us", "ca, us", "ny, us", "tx, us", "ga, us", "nc, us", "va, us"]):
                return True
        elif iso_code == "au" or "australia" in country_name:
            if any(term in combined for term in [", au", "australia", "sydney", "melbourne", "brisbane"]):
                return True
        elif iso_code == "in" or "india" in country_name:
            if any(term in combined for term in [", in", "india", "mumbai", "delhi", "bangalore"]):
                return True
        elif iso_code == "fr" or "france" in country_name:
            if any(term in combined for term in [", fr", "france", "paris", "rouen"]):
                return True
        elif iso_code == "es" or "spain" in country_name:
            if any(term in combined for term in [", es", "spain", "madrid", "barcelona"]):
                return True
        elif iso_code == "de" or "germany" in country_name:
            if any(term in combined for term in [", de", "germany", "berlin", "munich"]):
                return True

        # 2. General ISO2 code match if not caught by specific handlers above
        if iso_code and len(iso_code) == 2:
            if re.search(r'\b' + re.escape(iso_code) + r'\b', combined):
                return True

        # 3. Match Country name substring
        if country_name and len(country_name) > 3 and country_name in combined:
            return True

        return False

    def _matches_platform(self, platform_str: str) -> bool:
        """
        Checks whether creator's social platform matches the target platform filter.
        """
        if not self.target_platform or any(
            p in self.target_platform.lower() 
            for p in ["all", "instagram & tiktok", "both"]
        ):
            return True

        target = self.target_platform.lower()
        creator_p = (platform_str or "").lower()

        if "instagram only" in target:
            return "instagram" in creator_p
        elif "tiktok only" in target:
            return "tiktok" in creator_p
        elif "youtube" in target:
            return "youtube" in creator_p

        return True

    def evaluate_influencer(self, row: pd.Series) -> Tuple[str, str]:
        """
        Evaluates a single influencer row against all criteria:
        Follower count, Engagement rate, Niche/Brand fit, Audience Geography, Platform.
        Returns: (status: 'PASSED' | 'FAILED', reason: str)
        """
        followers = int(row.get("follower_count", 0))
        engagement = float(row.get("engagement_rate", 0.0))
        niche = str(row.get("niche", ""))
        bio = str(row.get("bio", ""))
        geo = str(row.get("audience_geography", row.get("location", "Not Specified")))
        loc = str(row.get("location", ""))
        platform = str(row.get("platform", "Instagram"))

        rejection_reasons = []

        # 1. Follower Count Check (Micro-influencer: 5,000 - 100,000)
        if followers < self.min_followers:
            rejection_reasons.append(
                f"Follower count {followers:,} is below minimum threshold ({self.min_followers:,})"
            )
        elif followers > self.max_followers:
            rejection_reasons.append(
                f"Follower count {followers:,} exceeds micro-influencer ceiling ({self.max_followers:,})"
            )

        # 2. Engagement Rate Check
        if engagement < self.min_engagement:
            rejection_reasons.append(
                f"Engagement rate {engagement:.2f}% is below required threshold ({self.min_engagement:.2f}%)"
            )

        # 3. Brand-Fit & Category Check
        target_tokens = [t.lower() for t in self.target_niche.replace("&", "").split() if len(t) > 2]
        content_context = (niche + " " + bio + " " + str(row.get("content_themes", ""))).lower()
        matches = [t for t in target_tokens if t in content_context]
        if not matches and len(target_tokens) > 0:
            rejection_reasons.append(
                f"Content context does not strongly match target category '{self.target_niche}'"
            )

        # 4. Audience Geography Filter Check
        if not self._matches_geography(geo, loc):
            rejection_reasons.append(
                f"Audience geography '{geo}' does not match target '{self.target_geography}'"
            )

        # 5. Platform Filter Check
        if not self._matches_platform(platform):
            rejection_reasons.append(
                f"Platform '{platform}' does not match target filter '{self.target_platform}'"
            )

        if rejection_reasons:
            return "FAILED", " | ".join(rejection_reasons)
        else:
            return "PASSED", f"Qualified: {followers:,} followers, {engagement:.2f}% engagement, strong fit for {self.target_niche} in {geo}"

    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies filtering logic to the entire dataset and adds qualification columns.
        """
        statuses = []
        reasons = []

        for _, row in df.iterrows():
            status, reason = self.evaluate_influencer(row)
            statuses.append(status)
            reasons.append(reason)

        df["qualification_status"] = statuses
        df["qualification_reason"] = reasons

        # Save processed dataset
        df.to_csv(PROCESSED_DATA_PATH, index=False)
        return df

if __name__ == "__main__":
    if RAW_DATA_PATH.exists():
        raw_df = pd.read_csv(RAW_DATA_PATH)
        classifier = InfluencerClassifier(target_geography="United States (US)")
        result_df = classifier.process_dataset(raw_df)
        passed = (result_df["qualification_status"] == "PASSED").sum()
        failed = (result_df["qualification_status"] == "FAILED").sum()
        print(f"Classification test complete! Total: {len(result_df)} | Passed: {passed} | Failed: {failed}")
    else:
        print("Raw data not found. Please run discovery first.")
