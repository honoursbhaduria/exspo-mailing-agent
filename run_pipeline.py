#!/usr/bin/env python3
"""
EDXSO AI Engineer Intern – Assignment 1
Automated Micro-Influencer Outreach System Pipeline CLI
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

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

console = Console()

def run_full_pipeline(niche: str = DEFAULT_NICHE, crawl_new: bool = False):
    console.print(Panel.fit(
        f"[bold blue]EDXSO Automated Micro-Influencer Outreach Pipeline[/bold blue]\n"
        f"Target Niche: [cyan]{niche}[/cyan] | Follower Range: [cyan]{MIN_FOLLOWERS:,} - {MAX_FOLLOWERS:,}[/cyan]\n"
        f"Min Engagement: [cyan]{MIN_ENGAGEMENT_RATE}%[/cyan] | Mode: [yellow]{'Simulation (Safe)' if SIMULATION_MODE else 'Live Resend API'}[/yellow]",
        title="Pipeline Initializing"
    ))

    # Phase 1: Influencer Discovery
    console.print("\n[bold yellow]Step 1: Discovering Influencers via Scrapy...[/bold yellow]")
    if crawl_new or not RAW_DATA_PATH.exists():
        raw_df = run_discovery_cli(niche=niche, limit=65)
    else:
        raw_df = pd.read_csv(RAW_DATA_PATH)
        console.print(f"Loaded existing dataset from [green]{RAW_DATA_PATH}[/green]")

    console.print(f"✓ Discovered [bold green]{len(raw_df)}[/bold green] influencer profiles.")

    # Phase 2: Profile Enrichment
    console.print("\n[bold yellow]Step 2: Profile Enrichment & Theme Extraction...[/bold yellow]")
    enricher = ProfileEnricher()
    enriched_df = enricher.enrich_dataset(raw_df)
    console.print("✓ Enriched profiles with content themes, demographics, and verified emails.")

    # Phase 3: Filtering & Classification
    console.print("\n[bold yellow]Step 3: Filtering & Classification...[/bold yellow]")
    classifier = InfluencerClassifier(
        min_followers=MIN_FOLLOWERS,
        max_followers=MAX_FOLLOWERS,
        min_engagement=MIN_ENGAGEMENT_RATE,
        target_niche=niche
    )
    classified_df = classifier.process_dataset(enriched_df)
    
    passed_df = classified_df[classified_df["qualification_status"] == "PASSED"]
    failed_df = classified_df[classified_df["qualification_status"] == "FAILED"]
    console.print(f"✓ Classification complete: [bold green]{len(passed_df)} Passed[/bold green] | [bold red]{len(failed_df)} Failed[/bold red]")

    # Phase 4: Message Personalization
    console.print("\n[bold yellow]Step 4: AI Message Personalization (Email & IG DM)...[/bold yellow]")
    generator = OutreachMessageGenerator()
    tracker = OutreachTracker()
    email_sender = EmailSender()
    ig_sender = InstagramDMSender()

    # Process shortlisted influencers (e.g., top 15 for demo run)
    shortlist_sample = passed_df.head(15)
    messages_generated = 0
    sent_count = 0

    table = Table(title="Outreach Dispatch Results", show_lines=True)
    table.add_column("Influencer", style="cyan", no_wrap=True)
    table.add_column("Handle", style="magenta")
    table.add_column("Followers", style="green")
    table.add_column("Email Status", style="blue")
    table.add_column("Email Pitch (60-90w)", style="white")
    table.add_column("IG DM (15-30w)", style="yellow")
    table.add_column("Dispatch Status", style="bold green")

    for _, influencer in shortlist_sample.iterrows():
        name = influencer["name"]
        handle = influencer["handle"]
        email = influencer["contact_email"]
        followers = f"{influencer['follower_count']:,}"

        # Deduplication check
        if tracker.has_been_contacted(handle) or tracker.has_been_contacted(email):
            console.print(f"Skipping duplicate: [cyan]{name}[/cyan] already contacted.")
            continue

        # Generate Dual Messages
        msg = generator.generate_messages(influencer.to_dict())
        messages_generated += 1

        email_pitch = msg["email_pitch"]
        ig_dm = msg["instagram_dm"]
        subject = msg["subject"]

        # Send or Simulate Email
        if email != "Not Found":
            dispatch_res = email_sender.send_email(
                to_email=email,
                subject=subject,
                message_body=email_pitch,
                recipient_name=name
            )
            status = dispatch_res["status"]
            delivery_id = dispatch_res.get("delivery_id", "N/A")
            channel = dispatch_res.get("channel", "Email")
            sent = status in ["SENT", "SENT (Simulated)"]
        else:
            # Route to Compliant IG DM Workflow
            dispatch_res = ig_sender.send_simulated_dm(handle, ig_dm)
            status = dispatch_res["status"]
            delivery_id = dispatch_res.get("delivery_id", "N/A")
            channel = dispatch_res.get("channel", "Instagram Direct")
            sent = True

        if sent:
            sent_count += 1

        tracker.log_outreach(
            influencer_name=name,
            handle=handle,
            email=email,
            platform=influencer["platform"],
            email_pitch=email_pitch,
            instagram_dm=ig_dm,
            channel=channel,
            sent=sent,
            status=status,
            delivery_id=delivery_id,
            notes=influencer["qualification_reason"]
        )

        table.add_row(
            name,
            f"@{handle}",
            followers,
            email if email != "Not Found" else "[red]Not Found (DM Only)[/red]",
            email_pitch[:80] + "...",
            ig_dm,
            f"[{'green' if sent else 'red'}]{status}[/{'green' if sent else 'red'}]"
        )

    console.print(table)
    console.print(f"\n[bold green]Pipeline finished successfully![/bold green] Processed {messages_generated} messages, {sent_count} outreach logs recorded.")
    console.print(f"Results saved to: [cyan]{OUTREACH_LOG_PATH}[/cyan]")

if __name__ == "__main__":
    run_full_pipeline()
