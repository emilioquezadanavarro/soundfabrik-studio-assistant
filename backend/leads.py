"""
Capture booking leads to Supabase.

Deliberately minimal: If a message contains an email or a phone number, it
stores the whole message verbatim alongside whatever contact fields it founds and a generic inquiry type

Structuring `message` further is left to a later step (an LLM classifier, an n8n workflow, or a human)
"""

from __future__ import annotations
import json
import re
from datetime import datetime, timezone
from backend.config import supabase_url, supabase_service_role_key
from supabase import create_client, Client

_client: Client | None = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(supabase_url(), supabase_service_role_key())
    return _client

# Finding e-mail information
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

# Finding phone information
# Optional "+", then digits with spaces / dashes / dots / parens
# Candidates are validated by digit count (see _find_phone)
PHONE_CANDIDATE_RE = re.compile(r"\+?\d[\d\s().\-]{6,}\d")

INQUIRY_TYPE = "general_inquiry"


def _find_email(text: str) -> str | None:
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None


def _find_phone(text: str) -> str | None:
    for m in PHONE_CANDIDATE_RE.finditer(text):
        digits = re.sub(r"\D", "", m.group())
        if 9 <= len(digits) <= 15:  # real phone numbers, E.164-ish
            return m.group().strip()
    return None


def extract_lead(text: str) -> dict | None:
    """Return {type, email, phone, message} if the text has an email or phone, else None."""
    email = _find_email(text)
    phone = _find_phone(text)
    if not email and not phone:
        return None
    return {
        "type": INQUIRY_TYPE,
        "email": email,
        "phone": phone,
        "message": text.strip(),
    }


def save_lead(lead: dict) -> dict:
    record = {
        "type": lead.get("type", INQUIRY_TYPE),
        "email": lead.get("email"),
        "phone": lead.get("phone"),
        "message": lead.get("message", ""),
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source": "recording_studio_public_chatbot",
    }

    try:
        _get_client().table("leads").insert(record).execute()
        print(f"[LEAD SAVED] {json.dumps(record)}")
    except Exception as e:
        print(f"[LEAD SAVE FAILED] {e} - record: {json.dumps(record)}")

    return record
