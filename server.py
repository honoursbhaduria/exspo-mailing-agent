import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    OUTREACH_LOG_PATH,
    DEFAULT_NICHE,
    MIN_FOLLOWERS,
    MAX_FOLLOWERS,
    MIN_ENGAGEMENT_RATE,
    SIMULATION_MODE
)
from src.discovery.runner import run_discovery_cli
from src.filtering.classifier import InfluencerClassifier
from src.enrichment.enricher import ProfileEnricher
from src.personalization.generator import OutreachMessageGenerator
from src.sending.sender import EmailSender, InstagramDMSender
from src.sending.tracker import OutreachTracker

app = FastAPI(
    title="EDXSO Micro-Influencer Outreach Backend API",
    description="RESTful API for Influencer Discovery, Classification, Enrichment, AI Personalization, and Delivery",
    version="1.0.0"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------
class FilterRequest(BaseModel):
    min_followers: int = MIN_FOLLOWERS
    max_followers: int = MAX_FOLLOWERS
    min_engagement: float = MIN_ENGAGEMENT_RATE
    target_niche: str = DEFAULT_NICHE
    target_geography: Optional[str] = "Global (All Regions)"
    target_platform: Optional[str] = "All Platforms"

class PersonalizeRequest(BaseModel):
    influencer: Dict[str, Any]
    brand_name: str = "LumiGlow"
    collaboration_type: str = "UGC & Paid Showcase"

class SendEmailRequest(BaseModel):
    to_email: str
    subject: str
    message_body: str
    recipient_name: str = "Creator"
    handle: str = ""
    platform: str = "Instagram"
    instagram_dm: str = ""
    notes: str = ""

# -------------------------------------------------------------
# API ENDPOINTS
# -------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "EDXSO Micro-Influencer Outreach System API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "simulation_mode": SIMULATION_MODE
    }

@app.get("/api/influencers/raw")
def get_raw_influencers(limit: int = 100):
    if not RAW_DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="No raw influencer data found. Run discovery first.")
    df = pd.read_csv(RAW_DATA_PATH).fillna("")
    return {
        "total": len(df),
        "limit": limit,
        "influencers": df.head(limit).to_dict(orient="records")
    }

@app.post("/api/influencers/discover")
def trigger_discovery(
    niche: str = Query(DEFAULT_NICHE),
    limit: int = Query(65),
    engine: str = Query("scrapy")
):
    try:
        df = run_discovery_cli(niche=niche, limit=limit, engine=engine)
        df_clean = df.fillna("")
        return {
            "status": "success",
            "discovered_count": len(df),
            "niche": niche,
            "engine": engine,
            "sample": df_clean[["name", "handle", "follower_count", "engagement_rate"]].head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/influencers/filter")
def filter_influencers(req: FilterRequest):
    if not RAW_DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="Raw dataset not found.")
    
    raw_df = pd.read_csv(RAW_DATA_PATH)
    enricher = ProfileEnricher()
    enriched_df = enricher.enrich_dataset(raw_df)

    classifier = InfluencerClassifier(
        min_followers=req.min_followers,
        max_followers=req.max_followers,
        min_engagement=req.min_engagement,
        target_niche=req.target_niche,
        target_geography=req.target_geography or "Global (All Regions)",
        target_platform=req.target_platform or "All Platforms"
    )
    processed_df = classifier.process_dataset(enriched_df).fillna("")

    passed = processed_df[processed_df["qualification_status"] == "PASSED"]
    failed = processed_df[processed_df["qualification_status"] == "FAILED"]

    return {
        "total": len(processed_df),
        "total_evaluated": len(processed_df),
        "passed_count": len(passed),
        "failed_count": len(failed),
        "target_geography": req.target_geography,
        "target_platform": req.target_platform,
        "results": processed_df.to_dict(orient="records"),
        "passed_influencers": passed.to_dict(orient="records"),
        "failed_influencers": failed.to_dict(orient="records")
    }

@app.post("/api/personalize")
def generate_personalization(req: PersonalizeRequest):
    generator = OutreachMessageGenerator()
    result = generator.generate_messages(
        influencer=req.influencer,
        brand_name=req.brand_name,
        collaboration_type=req.collaboration_type
    )
    return result

@app.post("/api/outreach/send")
def send_outreach(req: SendEmailRequest):
    email_sender = EmailSender()
    tracker = OutreachTracker()

    if tracker.has_been_contacted(req.handle) or tracker.has_been_contacted(req.to_email):
        return {
            "status": "SKIPPED",
            "message": f"Creator {req.recipient_name} (@{req.handle}) has already been contacted. Duplicate outreach prevented."
        }

    if req.to_email != "Not Found":
        dispatch_res = email_sender.send_email(
            to_email=req.to_email,
            subject=req.subject,
            message_body=req.message_body,
            recipient_name=req.recipient_name
        )
        status = dispatch_res["status"]
        delivery_id = dispatch_res.get("delivery_id")
        channel = dispatch_res.get("channel", "Email")
        sent = status in ["SENT", "SENT (Simulated)"]
    else:
        ig_sender = InstagramDMSender()
        dispatch_res = ig_sender.send_simulated_dm(req.handle, req.instagram_dm)
        status = "SENT_MANUALLY" if "manual" in req.notes.lower() else dispatch_res["status"]
        delivery_id = dispatch_res.get("delivery_id")
        channel = "Instagram Direct"
        sent = True

    tracker.log_outreach(
        influencer_name=req.recipient_name,
        handle=req.handle,
        email=req.to_email,
        platform=req.platform,
        email_pitch=req.message_body,
        instagram_dm=req.instagram_dm,
        channel=channel,
        sent=sent,
        status=status,
        delivery_id=delivery_id,
        notes=req.notes
    )

    return {
        "status": status,
        "delivery_id": delivery_id,
        "channel": channel,
        "sent": sent
    }

@app.get("/api/outreach/tracker")
def get_outreach_tracker():
    tracker = OutreachTracker()
    log_df = tracker._load_log().fillna("")
    stats = tracker.get_stats()
    return {
        "stats": stats,
        "logs": log_df.to_dict(orient="records")
    }

CACHED_COUNTRIES = []

@app.get("/api/geo/countries")
def get_countries():
    """
    Returns full list of all existing countries in the world using open-source API
    (https://countriesnow.space/api/v0.1/countries/iso) with fallback.
    """
    global CACHED_COUNTRIES
    if CACHED_COUNTRIES:
        return {"total": len(CACHED_COUNTRIES), "countries": CACHED_COUNTRIES}

    import requests
    default_countries = [
        "Global (All Regions)",
        "United States (US)",
        "United Kingdom (GB)",
        "Canada (CA)",
        "Australia (AU)",
        "Germany (DE)",
        "France (FR)",
        "India (IN)",
        "Italy (IT)",
        "Spain (ES)",
        "Japan (JP)",
        "Brazil (BR)",
        "Mexico (MX)",
        "Netherlands (NL)",
        "United Arab Emirates (AE)",
        "Singapore (SG)"
    ]

    try:
        res = requests.get("https://countriesnow.space/api/v0.1/countries/iso", timeout=4)
        if res.ok:
            data = res.json().get("data", [])
            fetched = []
            for item in data:
                c_name = item.get("name")
                c_iso = item.get("Iso2")
                if c_name:
                    label = f"{c_name} ({c_iso})" if c_iso else c_name
                    fetched.append(label)
            if fetched:
                fetched.sort()
                top_priority = ["United States (US)", "United Kingdom (GB)", "Canada (CA)", "Australia (AU)", "Germany (DE)", "France (FR)", "India (IN)"]
                for p in reversed(top_priority):
                    if p in fetched:
                        fetched.remove(p)
                    fetched.insert(0, p)
                CACHED_COUNTRIES = ["Global (All Regions)"] + fetched
                return {"total": len(CACHED_COUNTRIES), "countries": CACHED_COUNTRIES}
    except Exception as e:
        print(f"Notice: countriesnow API fallback engaged: {e}")

    CACHED_COUNTRIES = default_countries
    return {"total": len(CACHED_COUNTRIES), "countries": CACHED_COUNTRIES}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
