import re
import pandas as pd
from typing import Dict, Any

class ProfileEnricher:
    """
    Enriches influencer profiles with mandatory and optional context:
    - Content themes extraction
    - Strict email verification (marked 'Not Found' if absent)
    - Social platform links
    - Audience demographics inference (Age, Gender, Geography)
    """

    DEMOGRAPHIC_BENCHMARKS = {
        "Fashion & Beauty": {"age": "18-34 (72%)", "gender": "Female (78%)"},
        "Technology & AI": {"age": "21-40 (68%)", "gender": "Male (65%)"},
        "Fitness & Wellness": {"age": "20-38 (74%)", "gender": "Female (58%)"},
        "Lifestyle & Travel": {"age": "22-45 (70%)", "gender": "Female (62%)"},
        "Fintech & Crypto": {"age": "24-42 (75%)", "gender": "Male (72%)"}
    }

    def enrich_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        enriched = dict(record)

        # 0. Clean Name if corrupted by card text badges
        name = str(enriched.get("name", "")).strip()
        handle = str(enriched.get("handle", "")).strip()
        if not name or name in ["5.0", "UGC", "None"] or "top creator" in name.lower() or any(c in name for c in ["$", "%", "★"]):
            name = handle.replace("-", " ").replace("_", " ").title()
        enriched["name"] = name

        # 1. Clean & Verify Email
        email = str(enriched.get("contact_email", "")).strip()
        if not self._is_valid_email(email):
            enriched["contact_email"] = "Not Found"
        else:
            enriched["contact_email"] = email

        # 2. Extract / Standardize Content Themes
        bio = str(enriched.get("bio", ""))
        niche = str(enriched.get("niche", "Fashion & Beauty"))
        if not enriched.get("content_themes") or enriched.get("content_themes") == "Fashion, Lifestyle, UGC":
            enriched["content_themes"] = self._extract_themes_from_bio(bio, niche)

        # 3. Audience Demographics (Geography, Age, Gender)
        location = str(enriched.get("location", "Not Specified"))
        if location in ["", "None", "nan"]:
            enriched["audience_geography"] = "United States / Global"
        else:
            enriched["audience_geography"] = location

        niche_key = "Fashion & Beauty"
        for k in self.DEMOGRAPHIC_BENCHMARKS:
            if any(term in niche.lower() for term in k.lower().split()):
                niche_key = k
                break

        benchmarks = self.DEMOGRAPHIC_BENCHMARKS[niche_key]
        enriched["audience_age"] = benchmarks["age"]
        enriched["audience_gender"] = benchmarks["gender"]

        # 4. Standardize Platform URLs
        handle = str(enriched.get("handle", "")).strip()
        if not enriched.get("instagram_url") and handle:
            enriched["instagram_url"] = f"https://instagram.com/{handle}"
        if not enriched.get("tiktok_url") and handle:
            enriched["tiktok_url"] = f"https://tiktok.com/@{handle}"

        return enriched

    def enrich_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        enriched_rows = [self.enrich_record(row.to_dict()) for _, row in df.iterrows()]
        return pd.DataFrame(enriched_rows)

    def _is_valid_email(self, email: str) -> bool:
        if not email or email == "Not Found" or "@" not in email:
            return False
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, email):
            return False
        invalid_domains = ["collabstr.com", "example.com", "sentry.io", "w3.org", "domain.com", "lucide", "chart.js", ".png", ".jpg", ".webp", ".svg"]
        return not any(d in email.lower() for d in invalid_domains)

    def _extract_themes_from_bio(self, bio: str, niche: str) -> str:
        bio_lower = bio.lower()
        themes = []
        
        keywords = {
            "Clean Beauty": ["clean", "vegan", "cruelty-free", "organic"],
            "Skincare Routine": ["skincare", "serum", "spf", "dermatology", "glow"],
            "Everyday Glam": ["makeup", "glam", "beauty", "cosmetics"],
            "Sustainable Fashion": ["sustainable", "thrift", "vintage", "slow fashion"],
            "Capsule Wardrobe": ["wardrobe", "ootd", "outfit", "styling", "lookbook"],
            "Home & Wellness": ["wellness", "health", "mindfulness", "lifestyle"],
            "UGC Product Testing": ["ugc", "review", "unboxing", "demo"]
        }

        for theme, words in keywords.items():
            if any(w in bio_lower for w in words):
                themes.append(theme)

        if not themes:
            themes = ["Everyday Styling", "UGC Reviews", "Lifestyle Aesthetics"]

        return ", ".join(themes[:3])
