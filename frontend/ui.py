"""Brand CSS and page chrome, matched to soundfabrikberlin.com """

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import streamlit as st

from backend.config import LOGO_MARK, STUDIO_ADDRESS, STUDIO_NAME, STUDIO_WEBSITE


def _data_uri(path: Path) -> str:
    """Embed a local image so HTML/CSS can display it without remote URLs."""
    mime, _ = mimetypes.guess_type(str(path))
    if path.suffix.lower() == ".svg":
        mime = "image/svg+xml"
    mime = mime or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def apply_brand_styles() -> None:
    """Inject CSS aligned with the official Soundfabrik Berlin site palette."""
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Libre+Franklin:wght@300;400;500;600&display=swap');

:root {
  --sf-bg: #eddcd3;
  --sf-ink: #260d00;
  --sf-body: #655147;
  --sf-muted: #948075;
  --sf-taupe: #695c59;
  --sf-orange: #c46e36;
  --sf-orange-deep: #a95c2a;
  --sf-surface: rgba(255, 255, 255, 0.55);
  --sf-surface-strong: rgba(255, 255, 255, 0.8);
  --sf-line: rgba(38, 13, 0, 0.12);
  --sf-font-display: "Instrument Sans", "Libre Franklin", sans-serif;
  --sf-font-body: "Libre Franklin", "Instrument Sans", sans-serif;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
  background: var(--sf-bg) !important;
  color: var(--sf-body) !important;
  font-family: var(--sf-font-body) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { visibility: hidden; height: 0; }

.block-container {
  padding-top: 1.6rem !important;
  padding-bottom: 6rem !important;
  max-width: 760px !important;
}

.sf-hero {
  text-align: center;
  padding: 0.4rem 0 1.4rem;
  border-bottom: 1px solid var(--sf-line);
  margin-bottom: 1.4rem;
  animation: sf-fade-up 0.7s ease-out both;
}
.sf-hero .sf-mark {
  height: 56px;
  width: 56px;
  object-fit: contain;
  margin: 0 auto 0.9rem;
  display: block;
}
.sf-hero h1 {
  font-family: var(--sf-font-display) !important;
  font-weight: 500 !important;
  font-size: clamp(1.75rem, 4vw, 2.35rem) !important;
  letter-spacing: -0.025em;
  text-transform: uppercase;
  color: var(--sf-ink) !important;
  margin: 0 0 0.4rem 0 !important;
  line-height: 1.15 !important;
}
.sf-hero p {
  margin: 0;
  color: var(--sf-muted);
  font-size: 0.98rem;
  font-weight: 400;
  letter-spacing: 0.01em;
}
.sf-tag {
  display: inline-block;
  margin-top: 0.85rem;
  font-family: var(--sf-font-display);
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--sf-orange);
}

div[data-testid="stChatMessage"] {
  background: var(--sf-surface) !important;
  border: 1px solid var(--sf-line) !important;
  border-radius: 2px !important;
  padding: 0.85rem 1rem !important;
  margin-bottom: 0.65rem !important;
  animation: sf-fade-up 0.45s ease-out both;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] span {
  color: var(--sf-body) !important;
  font-family: var(--sf-font-body) !important;
  font-size: 0.98rem !important;
  line-height: 1.55 !important;
}
div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong {
  color: var(--sf-ink) !important;
  font-weight: 600;
}
span[data-testid="stIconMaterial"],
[class*="material-symbols"],
[class*="material-icons"] {
  font-family: "Material Symbols Rounded", "Material Icons" !important;
}
div[data-testid="stChatMessageAvatarUser"] {
  background-color: var(--sf-orange) !important;
  color: #fff !important;
}

div.stButton > button {
  background: var(--sf-orange) !important;
  color: #fff !important;
  border: 1px solid transparent !important;
  border-radius: 2px !important;
  font-family: var(--sf-font-display) !important;
  font-weight: 600 !important;
  letter-spacing: 0.02em !important;
  padding: 0.7rem 1rem !important;
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
  box-shadow: none !important;
}
div.stButton > button:hover {
  background: var(--sf-orange-deep) !important;
  color: #fff !important;
  border-color: transparent !important;
  transform: translateY(-1px);
}
div.stButton > button:focus {
  box-shadow: 0 0 0 2px rgba(196, 110, 54, 0.45) !important;
}

[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
[data-testid="stChatInput"] {
  background: var(--sf-bg) !important;
}
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] div[contenteditable="true"] {
  color: var(--sf-ink) !important;
  caret-color: var(--sf-orange) !important;
  font-family: var(--sf-font-body) !important;
}
[data-testid="stChatInput"] > div {
  background: #fff !important;
  border: 1px solid var(--sf-line) !important;
  border-radius: 2px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--sf-muted) !important; }
[data-testid="stChatInputSubmitButton"] { color: var(--sf-orange) !important; }
[data-testid="stChatInputSubmitButton"]:hover {
  background: rgba(196, 110, 54, 0.12) !important;
  color: var(--sf-orange-deep) !important;
}

div[data-testid="stAlert"] {
  background: var(--sf-surface-strong) !important;
  border: 1px solid var(--sf-orange) !important;
  color: var(--sf-ink) !important;
  border-radius: 2px !important;
}
div[data-testid="stAlert"] p { color: var(--sf-ink) !important; }

[data-testid="stSpinner"] p,
[data-testid="stSpinner"] div { color: var(--sf-body) !important; }

.sf-footer {
  text-align: center;
  margin-top: 1.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--sf-line);
  color: var(--sf-taupe);
  font-size: 0.78rem;
  letter-spacing: 0.02em;
}
.sf-footer a {
  color: var(--sf-body);
  text-decoration: none;
  border-bottom: 1px solid rgba(196, 110, 54, 0.5);
}
.sf-footer a:hover { color: var(--sf-orange); }

@keyframes sf-fade-up {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }
</style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    mark_src = _data_uri(LOGO_MARK) if LOGO_MARK.exists() else ""
    mark_html = (
        f'<img class="sf-mark" src="{mark_src}" alt="{STUDIO_NAME} logo" />'
        if mark_src
        else ""
    )
    st.markdown(
        f"""
<div class="sf-hero">
  {mark_html}
  <h1>{STUDIO_NAME}</h1>
  <p>The prime recording studio in the heart of the capital</p>
  <span class="sf-tag">Franz · Studio assistant</span>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    website_label = STUDIO_WEBSITE.rstrip("/").split("://", 1)[-1]
    st.markdown(
        f"""
<div class="sf-footer">
  {STUDIO_ADDRESS} ·
  <a href="{STUDIO_WEBSITE}" target="_blank" rel="noopener">{website_label}</a>
</div>
        """,
        unsafe_allow_html=True,
    )
