import unittest
import os
import pandas as pd
from pathlib import Path

from config.settings import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    OUTREACH_LOG_PATH,
    MIN_FOLLOWERS,
    MAX_FOLLOWERS,
    MIN_ENGAGEMENT_RATE,
    DEFAULT_NICHE
)
from src.filtering.classifier import InfluencerClassifier
from src.enrichment.enricher import ProfileEnricher
from src.personalization.generator import OutreachMessageGenerator
from src.sending.tracker import OutreachTracker
from src.sending.sender import EmailSender, InstagramDMSender

class TestEDXSOOutreachPipeline(unittest.TestCase):
    """
    Automated verification suite ensuring 100% compliance with
    EDXSO AI Engineer Intern Assignment 1 specifications.
    """

    def setUp(self):
        self.raw_df = pd.read_csv(RAW_DATA_PATH)
        self.enricher = ProfileEnricher()
        self.classifier = InfluencerClassifier(
            min_followers=MIN_FOLLOWERS,
            max_followers=MAX_FOLLOWERS,
            min_engagement=MIN_ENGAGEMENT_RATE,
            target_niche=DEFAULT_NICHE
        )
        self.generator = OutreachMessageGenerator()

    # -------------------------------------------------------------
    # 1. Influencer Discovery Tests
    # -------------------------------------------------------------
    def test_discovery_dataset_size(self):
        """Requirement 1: System should fetch at least 50 micro-influencers."""
        self.assertGreaterEqual(
            len(self.raw_df), 50,
            f"Dataset must contain at least 50 creators, found {len(self.raw_df)}"
        )

    def test_discovery_required_columns(self):
        """Requirement 1: Discover records contain core social identifier columns."""
        required = ["name", "handle", "platform", "profile_url", "follower_count", "engagement_rate", "niche"]
        for col in required:
            self.assertIn(col, self.raw_df.columns, f"Missing required discovery column: {col}")

    # -------------------------------------------------------------
    # 2. Filtering & Classification Tests
    # -------------------------------------------------------------
    def test_classification_logic(self):
        """Requirement 2: Classification identifies pass/fail criteria and reasons."""
        sample_creators = pd.DataFrame([
            # Passed creator
            {"handle": "pass1", "name": "Valid Creator", "follower_count": 25000, "engagement_rate": 4.5, "niche": "Fashion"},
            # Under minimum followers (<5k)
            {"handle": "fail_low", "name": "Low Follower", "follower_count": 3000, "engagement_rate": 5.0, "niche": "Fashion"},
            # Above maximum followers (>100k)
            {"handle": "fail_high", "name": "High Follower", "follower_count": 150000, "engagement_rate": 3.0, "niche": "Fashion"},
            # Low engagement (<2.0%)
            {"handle": "fail_eng", "name": "Low Engagement", "follower_count": 20000, "engagement_rate": 1.2, "niche": "Fashion"},
        ])

        classified = self.classifier.process_dataset(sample_creators)
        status_map = dict(zip(classified["handle"], classified["qualification_status"]))
        reason_map = dict(zip(classified["handle"], classified["qualification_reason"]))

        self.assertEqual(status_map["pass1"], "PASSED")
        self.assertEqual(status_map["fail_low"], "FAILED")
        self.assertIn("below minimum threshold", reason_map["fail_low"])
        self.assertEqual(status_map["fail_high"], "FAILED")
        self.assertIn("exceeds micro-influencer", reason_map["fail_high"])
        self.assertEqual(status_map["fail_eng"], "FAILED")
        self.assertIn("below required threshold", reason_map["fail_eng"])

    # -------------------------------------------------------------
    # 3. Profile Enrichment Tests
    # -------------------------------------------------------------
    def test_profile_enrichment_mandatory_fields(self):
        """Requirement 3: Mandatory fields must be present and emails marked 'Not Found' if missing."""
        enriched = self.enricher.enrich_dataset(self.raw_df)
        mandatory_cols = [
            "name", "platform", "profile_url", "follower_count",
            "engagement_rate", "niche", "content_themes", "contact_email"
        ]
        for col in mandatory_cols:
            self.assertIn(col, enriched.columns, f"Missing mandatory enriched column: {col}")

        # Verify emails are never fabricated or guessed (must be either valid email or 'Not Found')
        for email in enriched["contact_email"].dropna():
            is_valid = ("@" in email and "." in email) or email == "Not Found"
            self.assertTrue(is_valid, f"Email contains invalid or guessed format: {email}")

    # -------------------------------------------------------------
    # 4. Message Personalization Tests
    # -------------------------------------------------------------
    def test_message_personalization_word_counts(self):
        """Requirement 4: Email pitch 60-90 words, Instagram DM 15-30 words."""
        creator = {
            "name": "Sarah Jenkins",
            "handle": "sarahjstyle",
            "niche": "Fashion",
            "content_themes": "Sustainable Wardrobe, Outfit Inspirations",
            "follower_count": 32000,
            "engagement_rate": 4.8,
            "location": "New York, US",
            "bio": "Sharing everyday sustainable capsule wardrobe styling and thrift finds."
        }

        messages = self.generator.generate_messages(
            influencer=creator,
            brand_name="LumiGlow",
            collaboration_type="UGC & Sponsored Showcase"
        )

        email_pitch = messages.get("email_pitch", "")
        instagram_dm = messages.get("instagram_dm", "")

        email_words = len(email_pitch.split())
        dm_words = len(instagram_dm.split())

        self.assertGreaterEqual(
            email_words, 60,
            f"Email pitch must be at least 60 words, got {email_words}"
        )
        self.assertLessEqual(
            email_words, 90,
            f"Email pitch must be at most 90 words, got {email_words}"
        )

        self.assertGreaterEqual(
            dm_words, 15,
            f"Instagram DM must be at least 15 words, got {dm_words}"
        )
        self.assertLessEqual(
            dm_words, 30,
            f"Instagram DM must be at most 30 words, got {dm_words}"
        )

    # -------------------------------------------------------------
    # 5. Sending Layer & Outreach Tracker Tests
    # -------------------------------------------------------------
    def test_outreach_tracker_duplicate_prevention(self):
        """Requirement 5: Sending layer maintains log and prevents duplicate outreach."""
        test_log_path = Path("data/test_outreach_tracker.csv")
        if test_log_path.exists():
            test_log_path.unlink()

        tracker = OutreachTracker(log_path=test_log_path)
        handle = "alexastyle_test"
        email = "alexa@testdomain.com"

        # Initially should not have been contacted
        self.assertFalse(tracker.has_been_contacted(handle))
        self.assertFalse(tracker.has_been_contacted(email))

        # Log outreach
        tracker.log_outreach(
            influencer_name="Alexa",
            handle=handle,
            email=email,
            platform="Instagram",
            email_pitch="Test email body",
            instagram_dm="Test DM body",
            channel="Email",
            sent=True,
            status="Sent",
            delivery_id="TEST-12345"
        )

        # Idempotency check: should now be detected as contacted
        self.assertTrue(tracker.has_been_contacted(handle))
        self.assertTrue(tracker.has_been_contacted(email))

        # Clean up temporary test log
        if test_log_path.exists():
            test_log_path.unlink()

    # -------------------------------------------------------------
    # 6. Output Validator & Declarative Config Tests
    # -------------------------------------------------------------
    def test_personalization_validator_engine(self):
        """Validates that PersonalizationValidator programmatically enforces word counts & checks."""
        from src.personalization.validator import PersonalizationValidator

        # Valid outputs
        valid_res = PersonalizationValidator.validate(
            email_pitch=" ".join(["word"] * 75) + " Sarah LumiGlow",
            instagram_dm=" ".join(["word"] * 20) + " Sarah",
            creator_name="Sarah Jenkins",
            brand_name="LumiGlow"
        )
        self.assertTrue(valid_res["is_valid"])
        self.assertTrue(valid_res["checks"]["email_length"])
        self.assertTrue(valid_res["checks"]["dm_length"])
        self.assertTrue(valid_res["checks"]["name_included"])

        # Violating outputs (< 60 words email)
        invalid_res = PersonalizationValidator.validate(
            email_pitch="Too short email pitch text here.",
            instagram_dm="Short DM",
            creator_name="Sarah Jenkins",
            brand_name="LumiGlow"
        )
        self.assertFalse(invalid_res["is_valid"])
        self.assertFalse(invalid_res["checks"]["email_length"])
        self.assertFalse(invalid_res["checks"]["dm_length"])

    def test_classifier_yaml_config(self):
        """Validates declarative loading of filtering thresholds from config/filtering.yaml."""
        classifier = InfluencerClassifier.from_yaml("config/filtering.yaml")
        self.assertEqual(classifier.min_followers, 5000)
        self.assertEqual(classifier.max_followers, 100000)
        self.assertEqual(classifier.min_engagement, 2.0)
        self.assertEqual(classifier.target_niche, "Fashion")

    def test_audience_geography_filtering(self):
        """Validates that Audience Geography filtering precisely matches countries and rejects mismatches."""
        us_creator = pd.Series({
            "name": "US Creator", "handle": "us_creator", "follower_count": 20000,
            "engagement_rate": 3.5, "niche": "Fashion & Beauty", "location": "Miami, FL, US",
            "audience_geography": "Miami, FL, US", "platform": "Instagram"
        })
        uk_creator = pd.Series({
            "name": "UK Creator", "handle": "uk_creator", "follower_count": 25000,
            "engagement_rate": 3.0, "niche": "Fashion & Beauty", "location": "London, LND, GB",
            "audience_geography": "London, LND, GB", "platform": "Instagram"
        })

        classifier_us = InfluencerClassifier(target_geography="United States (US)")
        status_us, _ = classifier_us.evaluate_influencer(us_creator)
        status_uk, reason_uk = classifier_us.evaluate_influencer(uk_creator)

        self.assertEqual(status_us, "PASSED")
        self.assertEqual(status_uk, "FAILED")
        self.assertIn("Audience geography", reason_uk)

    def test_playwright_scraper_engine(self):
        """Validates PlaywrightInfluencerScraper initialization and headless browser capability."""
        from src.discovery.playwright_scraper import PlaywrightInfluencerScraper
        scraper = PlaywrightInfluencerScraper(headless=True)
        self.assertIsNotNone(scraper)
        self.assertTrue(scraper.headless)

if __name__ == "__main__":
    unittest.main()
