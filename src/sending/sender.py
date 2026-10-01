import os
import time
import uuid
import re
from typing import Dict, Any, Optional
from config.settings import RESEND_API_KEY, SENDER_EMAIL, SIMULATION_MODE

class EmailSender:
    """
    Handles email outreach delivery via Resend API or Safe Simulation Mode.
    Ensures that real emails are only dispatched when explicitly configured.
    """
    def __init__(self, api_key: Optional[str] = None, sender_email: Optional[str] = None, simulation_mode: Optional[bool] = None):
        self.api_key = api_key or RESEND_API_KEY
        self.sender_email = sender_email or SENDER_EMAIL
        self.simulation_mode = simulation_mode if simulation_mode is not None else SIMULATION_MODE
        
        self.resend_client = None
        if self.api_key and not self.simulation_mode:
            try:
                import resend
                resend.api_key = self.api_key
                self.resend_client = resend
            except Exception as e:
                print(f"Notice: Resend SDK init failed: {e}. Defaulting to simulation mode.")
                self.simulation_mode = True

    def send_email(self, to_email: str, subject: str, message_body: str, recipient_name: str = "Creator") -> Dict[str, Any]:
        """
        Sends an outreach email to the target influencer.
        """
        # 1. Validation
        if not to_email or to_email == "Not Found":
            return {
                "status": "SKIPPED",
                "delivery_id": None,
                "error": "No contact email available for this influencer (Eligible for Instagram DM outreach)"
            }

        if not self._is_valid_email_format(to_email):
            return {
                "status": "FAILED",
                "delivery_id": None,
                "error": f"Invalid email format: '{to_email}'"
            }

        # 2. Live Resend Delivery
        if self.resend_client and not self.simulation_mode:
            try:
                params = {
                    "from": self.sender_email,
                    "to": [to_email],
                    "subject": subject,
                    "text": message_body,
                    "html": f"""
                    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; padding: 20px;">
                        {message_body.replace(chr(10), '<br/>')}
                    </div>
                    """
                }
                response = self.resend_client.Emails.send(params)
                delivery_id = response.get("id", str(uuid.uuid4()))
                return {
                    "status": "SENT",
                    "delivery_id": delivery_id,
                    "channel": "Resend API (Live)",
                    "error": None
                }
            except Exception as e:
                return {
                    "status": "FAILED",
                    "delivery_id": None,
                    "channel": "Resend API (Live)",
                    "error": str(e)
                }

        # 3. Simulated Delivery Mode (Safe Evaluation Mode)
        time.sleep(0.15)  # Simulate realistic API round-trip
        sim_id = f"sim_{uuid.uuid4().hex[:12]}"
        return {
            "status": "SENT (Simulated)",
            "delivery_id": sim_id,
            "channel": "Resend Sandbox Simulator",
            "error": None
        }

    def _is_valid_email_format(self, email: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))


class InstagramDMSender:
    """
    Demonstrates compliant Instagram DM workflow:
    - Formats copy-ready message with quick copy actions
    - Logs simulated DM delivery without violating Meta Graph API policies
    """
    def send_simulated_dm(self, handle: str, dm_text: str) -> Dict[str, Any]:
        sim_id = f"dm_sim_{uuid.uuid4().hex[:8]}"
        return {
            "status": "DM SENT (Simulated)",
            "delivery_id": sim_id,
            "handle": f"@{handle.lstrip('@')}",
            "channel": "Instagram Direct (Simulated/Manual Workflow)",
            "action_url": f"https://ig.me/m/{handle.lstrip('@')}",
            "error": None
        }
