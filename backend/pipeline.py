""" One turn: guard → retrieve → generate (and lead capture). No Streamlit """

from __future__ import annotations

from dataclasses import dataclass, field

from langsmith import traceable

from backend.config import (
    HISTORY_TURN_LIMIT,
    MAX_MESSAGE_CHARS,
    MAX_TURNS_PER_SESSION,
    STUDIO_NAME,
)
from backend.generate import generate_reply
from backend.guard import is_on_topic, looks_like_booking
from backend.ingestion import get_vectorstore
from backend.leads import extract_lead, save_lead
from backend.prompts import (
    LEAD_CAPTURE_PROMPT,
    MESSAGE_TOO_LONG_REPLY,
    OFF_TOPIC_REPLY,
    RATE_LIMIT_REPLY,
)
from backend.retrieve import format_context, retrieve_chunks, source_names

@dataclass
class SessionState:
    awaiting_lead: bool = False
    lead_captured: bool = False
    turn_count: int = 0

@dataclass
class TurnResult:
    reply: str
    sources: list[str] = field(default_factory=list)
    lead_saved: dict | None = None
    state: SessionState = field(default_factory=SessionState)


THANKS_REPLY = (
    f"Thank you! We've got your details. Our team at {STUDIO_NAME} will "
    "reach out with a custom quote soon. Meanwhile, feel free to "
    "ask anything else about the studios or our services."
)


@traceable(name="handle_turn", run_type="chain")
def handle_turn(user_text: str, history: list[dict], state: SessionState | None = None) -> TurnResult:
    """Answer one user message. `history` is prior turns only (not this message)."""
    state = state or SessionState()

    # Abuse guards, checked before anything else touches the LLM or Chroma.
    state.turn_count += 1
    if state.turn_count > MAX_TURNS_PER_SESSION:
        return TurnResult(reply=RATE_LIMIT_REPLY, state=state)
    if len(user_text) > MAX_MESSAGE_CHARS:
        return TurnResult(reply=MESSAGE_TOO_LONG_REPLY, state=state)

    # Cap how much prior context gets sent to the LLM, regardless of how long
    # the session has run — 2 messages (user + assistant) per turn.
    history = history[-(2 * HISTORY_TURN_LIMIT):]

    # Capture contact info whenever the visitor provides it, not only when we
    # explicitly asked. Franz may ask for it on his own, or the visitor may
    # volunteer it. As long as no lead is on file yet, an email or phone number
    # in the message is a lead.
    if not state.lead_captured:
        lead = extract_lead(user_text)
        if lead:
            save_lead(lead)
            state.lead_captured = True
            state.awaiting_lead = False
            # The same message often also carries a real question. Answer it
            # instead of swallowing it behind a canned thank-you; THANKS_REPLY
            # is only the fallback if the generation call fails.
            store = get_vectorstore()
            chunks = retrieve_chunks(store, user_text)
            context = format_context(chunks)
            try:
                reply = generate_reply(
                    user_text,
                    history,
                    context,
                    lead_captured=True,
                    instruction=(
                        "The visitor just shared their contact details and they are "
                        "now on file; the team will follow up about booking. Briefly "
                        "thank them for the details, then answer any other question "
                        "in their message from the context. Do not ask for contact "
                        "details again."
                    ),
                )
            except Exception:
                reply = THANKS_REPLY
            return TurnResult(
                reply=reply,
                sources=source_names(chunks),
                lead_saved=lead,
                state=state,
            )

    # We asked for contact info last turn but this message didn't include any:
    # answer the question anyway and gently remind them.
    if state.awaiting_lead and not state.lead_captured:
        store = get_vectorstore()
        chunks = retrieve_chunks(store, user_text)
        context = format_context(chunks)
        nudge = (
                generate_reply(user_text, history, context)
                + "\n\nWhenever you're ready, just share your **email or phone number** "
                  "and we'll prepare that custom quote."
        )
        return TurnResult(reply=nudge, sources=source_names(chunks), state=state)

    if not is_on_topic(user_text, history):
        return TurnResult(reply=OFF_TOPIC_REPLY, state=state)

    if looks_like_booking(user_text) and not state.lead_captured:
        state.awaiting_lead = True
        store = get_vectorstore()
        chunks = retrieve_chunks(store, user_text)
        context = format_context(chunks)
        try:
            reply = generate_reply(
                user_text,
                history,
                context,
                instruction=(
                    "The visitor is asking about booking, rates, or availability. "
                    "Briefly acknowledge their specific question and note that rates "
                    "are quoted per project, then ask for their name plus an email or "
                    "phone number so the team can send a custom quote. Keep it to a "
                    "few sentences and stay in Franz's voice."
                ),
            )
        except Exception:
            reply = LEAD_CAPTURE_PROMPT
        return TurnResult(reply=reply, sources=source_names(chunks), state=state)

    store = get_vectorstore()
    chunks = retrieve_chunks(store, user_text)
    context = format_context(chunks)
    reply = generate_reply(user_text, history, context, lead_captured=state.lead_captured)
    return TurnResult(reply=reply, sources=source_names(chunks), state=state)