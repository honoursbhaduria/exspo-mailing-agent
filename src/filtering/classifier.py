import pandas as pd
from typing import Dict, Any, Tuple
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
    to qualify or disqualify them for brand collaboration outreach.
    """
    def __init__(
        self,
        min_followers: int = MIN_FOLLOWERS,
        max_followers: int = MAX_FOLLOWERS,
        min_engagement: float = MIN_ENGAGEMENT_RATE,
        target_niche: str = "Fashion & Beauty"
    ):
        self.min_followers = min_followers
        self.max_followers = max_followers
        self.min_engagement = min_engagement
        self.target_niche = target_niche

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
                    target_niche=cfg.get("niche", "Fashion & Beauty")
                )
        except Exception:
            pass
        return cls()

    def evaluate_influencer(self, row: pd.Series) -> Tuple[str, str]:
        """
        Evaluates a single influencer row.
        Returns: (status: 'PASSED' | 'FAILED', reason: str)
        """
        followers = int(row.get("follower_count", 0))
        engagement = float(row.get("engagement_rate", 0.0))
        niche = str(row.get("niche", ""))
        bio = str(row.get("bio", ""))

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

        # 2. Engagement Rate Check (>= 2.0%)
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

        if rejection_reasons:
            return "FAILED", " | ".join(rejection_reasons)
        else:
            return "PASSED", f"Qualified: {followers:,} followers, {engagement:.2f}% engagement, strong fit for {self.target_niche}"

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
        classifier = InfluencerClassifier()
        result_df = classifier.process_dataset(raw_df)
        passed = (result_df["qualification_status"] == "PASSED").sum()
        failed = (result_df["qualification_status"] == "FAILED").sum()
        print(f"Classification complete! Total: {len(result_df)} | Passed: {passed} | Failed: {failed}")
    else:
        print("Raw data not found. Please run discovery first.")
