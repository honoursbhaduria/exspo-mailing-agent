"""
EDXSO Micro-Influencer Outreach System
Personalization Output Validator

Ensures programmatically that generated LLM outreach meets exact EDXSO assignment constraints:
- Email pitch: strictly 60 to 90 words
- Instagram DM: strictly 15 to 30 words
- Evidence-based inclusion: Creator name, brand name, no template placeholders
"""

from typing import Dict, Any, List

class PersonalizationValidator:
    """
    Validates output text from LLMs and generators against strict assignment criteria.
    """

    MIN_EMAIL_WORDS = 60
    MAX_EMAIL_WORDS = 90
    MIN_DM_WORDS = 15
    MAX_DM_WORDS = 30

    @classmethod
    def validate(
        cls,
        email_pitch: str,
        instagram_dm: str,
        creator_name: str,
        brand_name: str = "LumiGlow"
    ) -> Dict[str, Any]:
        errors: List[str] = []
        checks = {}

        # 1. Word Count Checks
        email_words = len(email_pitch.split())
        dm_words = len(instagram_dm.split())

        email_length_valid = cls.MIN_EMAIL_WORDS <= email_words <= cls.MAX_EMAIL_WORDS
        if not email_length_valid:
            errors.append(f"Email pitch word count ({email_words}) violates [{cls.MIN_EMAIL_WORDS}-{cls.MAX_EMAIL_WORDS}] constraint.")
        checks["email_length"] = email_length_valid

        dm_length_valid = cls.MIN_DM_WORDS <= dm_words <= cls.MAX_DM_WORDS
        if not dm_length_valid:
            errors.append(f"Instagram DM word count ({dm_words}) violates [{cls.MIN_DM_WORDS}-{cls.MAX_DM_WORDS}] constraint.")
        checks["dm_length"] = dm_length_valid

        # 2. Evidence Verification (Creator's name)
        first_name = creator_name.split()[0].lower() if creator_name else ""
        name_in_email = first_name in email_pitch.lower()
        name_in_dm = first_name in instagram_dm.lower()
        name_included = name_in_email or name_in_dm
        if not name_included:
            errors.append(f"Neither pitch addresses creator by name '{first_name}'.")
        checks["name_included"] = name_included

        # 3. Brand Name Inclusion
        brand_included = brand_name.lower() in email_pitch.lower() or brand_name.lower() in instagram_dm.lower()
        if not brand_included:
            errors.append(f"Brand name '{brand_name}' not referenced.")
        checks["brand_included"] = brand_included

        # 4. Anti-Template / No Unfilled Placeholders
        placeholders = ["[insert", "{name}", "[brand", "[influencer", "<name>", "todo"]
        combined = (email_pitch + " " + instagram_dm).lower()
        has_placeholder = any(p in combined for p in placeholders)
        checks["no_placeholders"] = not has_placeholder
        if has_placeholder:
            errors.append("Unfilled bracketed template placeholder detected in generated pitch.")

        is_valid = len(errors) == 0

        return {
            "is_valid": is_valid,
            "checks": checks,
            "word_counts": {
                "email": email_words,
                "dm": dm_words,
                "email_range": f"{cls.MIN_EMAIL_WORDS}-{cls.MAX_EMAIL_WORDS}",
                "dm_range": f"{cls.MIN_DM_WORDS}-{cls.MAX_DM_WORDS}"
            },
            "errors": errors
        }
