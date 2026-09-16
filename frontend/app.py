"""
Studio Assistant — General Public Chatbot (Streamlit + LangChain + ChromaDB)

Deploy-ready for Streamlit Community Cloud. API keys via st.secrets or .env.

"""

from __future__ import annotations

import streamlit as st

from backend.config import LOGO_MARK, STUDIO_NAME
from backend.ingestion import get_vectorstore
from backend.pipeline import SessionState, handle_turn
from backend.prompts import GREETING, LEAD_CAPTURE_PROMPT

from frontend.secrets_bridge import bridge_secrets_to_env
from frontend.ui import apply_brand_styles, render_footer, render_hero


@st.cache_resource(show_spinner="Loading studio knowledge…")
def _cached_vectorstore():
    return get_vectorstore()


def init_session() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": GREETING},
        ]
    if "awaiting_lead" not in st.session_state:
        st.session_state.awaiting_lead = False
    if "lead_captured" not in st.session_state:
        st.session_state.lead_captured = False
    if "show_quick_replies" not in st.session_state:
        st.session_state.show_quick_replies = True
    if "pending_user" not in st.session_state:
        st.session_state.pending_user = None


def queue_user_turn(user_text: str) -> None:
    st.session_state.show_quick_replies = False
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.session_state.pending_user = user_text


def respond_to_user(user_text: str) -> None:
    state = SessionState(
        awaiting_lead=st.session_state.awaiting_lead,
        lead_captured=st.session_state.lead_captured,
    )
    result = handle_turn(
        user_text, st.session_state.messages[:-1], state=state
    )
    st.session_state.awaiting_lead = result.state.awaiting_lead
    st.session_state.lead_captured = result.state.lead_captured
    st.session_state.messages.append(
        {"role": "assistant", "content": result.reply}
    )


def main() -> None:
    st.set_page_config(
        page_title=f"Studio Assistant · {STUDIO_NAME}",
        page_icon=str(LOGO_MARK) if LOGO_MARK.exists() else None,
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    bridge_secrets_to_env()
    apply_brand_styles()
    render_hero()

    init_session()
    if (
        st.session_state.messages
        and st.session_state.messages[0]["role"] == "assistant"
        and "Franz" not in st.session_state.messages[0]["content"]
        and st.session_state.show_quick_replies
    ):
        st.session_state.messages[0]["content"] = GREETING

    try:
        _cached_vectorstore()
    except Exception as exc:
        st.error(f"Failed to build knowledge base: {exc}")
        st.stop()

    assistant_avatar = str(LOGO_MARK) if LOGO_MARK.exists() else None
    for msg in st.session_state.messages:
        avatar = assistant_avatar if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if st.session_state.pending_user:
        pending = st.session_state.pending_user
        st.session_state.pending_user = None
        with st.chat_message("assistant", avatar=assistant_avatar):
            with st.spinner("Franz is thinking…"):
                respond_to_user(pending)
        st.rerun()

    if st.session_state.show_quick_replies:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Explore Studio A & B", use_container_width=True):
                queue_user_turn(
                    "I'd like to explore Studio A and Studio B — "
                    "what are the differences and what is each best for?"
                )
                st.rerun()
        with col2:
            if st.button("Booking & Rates", use_container_width=True):
                st.session_state.awaiting_lead = True
                st.session_state.show_quick_replies = False
                st.session_state.messages.append(
                    {"role": "user", "content": "Booking & Rates"}
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": LEAD_CAPTURE_PROMPT}
                )
                st.rerun()

    # User input
    if prompt := st.chat_input("Ask Franz about studios, gear, services, or booking…"):
        queue_user_turn(prompt)
        st.rerun()

    render_footer()


if __name__ == "__main__":
    main()
