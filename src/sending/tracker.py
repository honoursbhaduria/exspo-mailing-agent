import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from config.settings import OUTREACH_LOG_PATH

class OutreachTracker:
    """
    Tracks and manages outreach history:
    - Maintains persistent log of messages, timestamps, channels, and delivery statuses
    - Prevents duplicate outreach to previously contacted creators or emails
    """
    def __init__(self, log_path: Path = OUTREACH_LOG_PATH):
        self.log_path = log_path
        self.log_df = self._load_log()

    def _load_log(self) -> pd.DataFrame:
        if self.log_path.exists():
            try:
                return pd.read_csv(self.log_path)
            except Exception:
                pass
        return pd.DataFrame(columns=[
            "influencer",
            "handle",
            "email",
            "platform",
            "message_generated",
            "instagram_dm",
            "channel",
            "sent",
            "date",
            "status",
            "delivery_id",
            "notes"
        ])

    def has_been_contacted(self, identifier: str) -> bool:
        """
        Checks if an influencer handle or email has already been contacted.
        """
        if self.log_df.empty or not identifier:
            return False
        
        id_clean = identifier.strip().lower()
        if id_clean == "not found":
            return False

        # Check handles and emails
        sent_logs = self.log_df[self.log_df["sent"] == True]
        handles = sent_logs["handle"].dropna().str.lower().tolist()
        emails = sent_logs["email"].dropna().str.lower().tolist()

        return id_clean in handles or id_clean in emails

    def log_outreach(
        self,
        influencer_name: str,
        handle: str,
        email: str,
        platform: str,
        email_pitch: str,
        instagram_dm: str,
        channel: str,
        sent: bool,
        status: str,
        delivery_id: Optional[str] = None,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Records a new outreach event to the log.
        """
        new_entry = {
            "influencer": influencer_name,
            "handle": handle,
            "email": email,
            "platform": platform,
            "message_generated": email_pitch,
            "instagram_dm": instagram_dm,
            "channel": channel,
            "sent": sent,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": status,
            "delivery_id": delivery_id or "N/A",
            "notes": notes
        }

        self.log_df = pd.concat([self.log_df, pd.DataFrame([new_entry])], ignore_index=True)
        self.save()
        return new_entry

    def save(self):
        self.log_df.to_csv(self.log_path, index=False)

    def get_stats(self) -> Dict[str, int]:
        total = len(self.log_df)
        sent = len(self.log_df[self.log_df["sent"] == True])
        skipped = len(self.log_df[self.log_df["status"].str.contains("SKIPPED", na=False)])
        failed = len(self.log_df[self.log_df["status"].str.contains("FAILED", na=False)])

        channels = self.log_df["channel"].fillna("").astype(str).str.lower()
        mail_sent = len(self.log_df[(self.log_df["sent"] == True) & (channels.str.contains("resend") | channels.str.contains("email"))])
        dm_sent = len(self.log_df[(self.log_df["sent"] == True) & (channels.str.contains("instagram") | channels.str.contains("dm"))])

        return {
            "total_logged": total,
            "successfully_sent": sent,
            "mail_sent": mail_sent,
            "dm_sent": dm_sent,
            "skipped": skipped,
            "failed": failed
        }
