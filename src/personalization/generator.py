import os
import json
import re
from typing import Dict, Any, Optional
from config.settings import GEMINI_API_KEY

class OutreachMessageGenerator:
    """
    Generates personalized collaboration pitches via Google Gemini LLM:
    1. Email Collaboration Pitch (60-90 words)
    2. Instagram DM (15-30 words)
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Could not initialize Gemini client: {e}")

    def generate_messages(self, influencer: Dict[str, Any], brand_name: str = "LumiGlow", collaboration_type: str = "UGC & Sponsored Showcase") -> Dict[str, Any]:
        """
        Generates personalized Email and Instagram DM messages.
        """
        name = influencer.get("name", "Creator")
        niche = influencer.get("niche", "Fashion & Beauty")
        themes = influencer.get("content_themes", "Styling, UGC")
        followers = influencer.get("follower_count", 15000)
        engagement = influencer.get("engagement_rate", 3.2)
        location = influencer.get("audience_geography", influencer.get("location", "US"))
        bio = influencer.get("bio", "")

        # Try LLM generation if Gemini client is initialized
        if self.client:
            try:
                return self._generate_with_gemini(
                    name=name,
                    niche=niche,
                    themes=themes,
                    followers=followers,
                    engagement=engagement,
                    location=location,
                    bio=bio,
                    brand_name=brand_name,
                    collaboration_type=collaboration_type
                )
            except Exception as e:
                print(f"LLM generation failed: {e}. Falling back to dynamic prompt generator.")

        # High-precision dynamic generator (fallback / offline mode)
        return self._generate_dynamic_fallback(
            name=name,
            niche=niche,
            themes=themes,
            followers=followers,
            engagement=engagement,
            location=location,
            bio=bio,
            brand_name=brand_name,
            collaboration_type=collaboration_type
        )

    def _generate_with_gemini(self, **kwargs) -> Dict[str, Any]:
        prompt = f"""
You are an expert Influencer Marketing Director for the brand '{kwargs['brand_name']}'.
Craft two personalized outreach messages for the following micro-influencer:

Creator Name: {kwargs['name']}
Niche: {kwargs['niche']}
Content Themes: {kwargs['themes']}
Follower Count: {kwargs['followers']:,}
Engagement Rate: {kwargs['engagement']}%
Audience Geography: {kwargs['location']}
Bio / Recent Content Focus: {kwargs['bio']}
Proposed Collaboration Angle: {kwargs['collaboration_type']}

MANDATORY CONSTRAINTS:
1. Email Pitch:
   - Length: EXACTLY between 60 and 90 words.
   - Reference their specific niche ({kwargs['niche']}) and content themes ({kwargs['themes']}).
   - Propose the collaboration ({kwargs['collaboration_type']}) and clear value proposition (paid fee + gifted items).
   - Professional, warm, and concise call to action.

2. Instagram DM:
   - Length: EXACTLY between 15 and 30 words.
   - Short, conversational, natural (sounds like a real human, not corporate spam).
   - Compliment a specific theme from their recent work.

Return ONLY a valid JSON object with the following schema:
{{
    "subject": "Email subject line",
    "email_pitch": "The 60-90 word email pitch text",
    "email_word_count": <number>,
    "instagram_dm": "The 15-30 word Instagram DM text",
    "dm_word_count": <number>,
    "collaboration_angle": "{kwargs['collaboration_type']}"
}}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = response.text.strip()
        # Clean potential markdown fences
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        data = json.loads(text.strip())
        data["email_word_count"] = len(data.get("email_pitch", "").split())
        data["dm_word_count"] = len(data.get("instagram_dm", "").split())
        return data

    def _generate_dynamic_fallback(self, **kwargs) -> Dict[str, Any]:
        first_name = kwargs["name"].split()[0]
        theme_list = [t.strip() for t in kwargs["themes"].split(",") if t.strip()]
        primary_theme = theme_list[0] if theme_list else kwargs["niche"]
        secondary_theme = theme_list[1] if len(theme_list) > 1 else "authentic content"

        # Email Pitch (60 - 90 words)
        subject = f"Collaboration with {kwargs['brand_name']} × {first_name}"
        email_pitch = (
            f"Hi {first_name},\n\n"
            f"I have been following your {primary_theme.lower()} content and love the thoughtful aesthetic you bring to your community. "
            f"Your focus on {secondary_theme.lower()} aligns seamlessly with our brand philosophy at {kwargs['brand_name']}.\n\n"
            f"We are launching a new paid campaign and would love to partner with you for a {kwargs['collaboration_type'].lower()}. "
            f"We offer competitive compensation alongside gifted product packages and custom affiliate perks for your audience.\n\n"
            f"Would you be open to reviewing the brief this week?\n\n"
            f"Best regards,\n"
            f"Partnerships Team | {kwargs['brand_name']}"
        )

        # Instagram DM (15 - 30 words)
        instagram_dm = (
            f"Hey {first_name}! Loved your recent posts on {primary_theme.lower()}. "
            f"Our team at {kwargs['brand_name']} would love to collaborate on our upcoming campaign. "
            f"Can we send the brief?"
        )

        email_words = len(email_pitch.split())
        dm_words = len(instagram_dm.split())

        return {
            "subject": subject,
            "email_pitch": email_pitch,
            "email_word_count": email_words,
            "instagram_dm": instagram_dm,
            "dm_word_count": dm_words,
            "collaboration_angle": kwargs["collaboration_type"]
        }
