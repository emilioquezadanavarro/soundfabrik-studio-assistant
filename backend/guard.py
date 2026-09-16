"""On-topic gate: regex fast path, then a small Claude classifier """

from __future__ import annotations

import re

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from langsmith import traceable

from backend.config import GUARD_MODEL, anthropic_api_key
from backend.generate import message_text
from backend.prompts import TOPIC_GUARD_PROMPT

STUDIO_TERMS = re.compile(
      r"\b("
      r"soundfabrik|studio\s*[ab]\b|studios?|salzufer|"
      r"live\s*room|control\s*room|iso\s*booth|isolation|lounge|"
      r"console|desk|pre\s*amps?|preamps?|microphones?|mics?|monitors?|speakers?|"
      r"outboard|compressors?|eq|plugins?|instruments?|piano|grand|drums?|"
      r"headphones?|cables?|patchbay|"
      r"neve|genesys|steinway|ludwig|atc|eve\s*audio|telefunken|urei|avalon|"
      r"millennia|tube\s*tech|distressor|la-?2a|la-?4|1176|dad|apollo|uad|"
      r"pro\s*tools|logic\s*pro|ssl|chandler|brent\s*averill|sta-?level|"
      r"record(?:ing|ings)?|mix(?:ing|es)?|master(?:ing)?|dolby|atmos|immersive|"
      r"7\.1\.4|surround|songwriting|overdub|tracking|sessions?|rehearsals?|"
      r"showcase|mastered|produce[rd]?|production|engineer|"
      r"book(?:ing)?|rates?|quote|availability|reserve|reservation|"
      r"load\s*in|parking|directions?|address"
      r")\b",
      re.IGNORECASE,
  )

BOOKING_KEYWORDS = re.compile(
    r"\b("
    r"book|booking|rates?|price|pricing|quote|availability|"
    r"reserve|reservation|session|hire|cost|how much"
    r")\b",
    re.IGNORECASE,
)

def looks_like_booking(text: str) -> bool:
    return bool(BOOKING_KEYWORDS.search(text))

def _guard_llm() -> ChatAnthropic:
    return ChatAnthropic(
        model=GUARD_MODEL,
        temperature=0,
        max_tokens=8,
        api_key=anthropic_api_key(),
    )

@traceable(name="guard_is_on_topic", run_type="chain")
def is_on_topic(user_message: str, history: list[dict]) -> bool:
    if STUDIO_TERMS.search(user_message):
        return True


    recent = "\n".join(
        f"{turn['role']}: {turn['content']}" for turn in history[-4:]
    )

    messages = [
        SystemMessage(content=TOPIC_GUARD_PROMPT),
        HumanMessage(
            content=(
                f"Conversation so far:\n{recent or '(none)'}\n\n"
                f"Latest visitor message:\n{user_message}"
            ),
       )
    ]

    try:
        verdict = message_text(_guard_llm().invoke(messages).content).strip().upper()
    except Exception:
        return True
    return not verdict.startswith("REFUSE")
