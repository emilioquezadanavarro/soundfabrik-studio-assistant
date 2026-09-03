"""Claude generation from retrieved context, with a web-search fallback tool """

from __future__ import annotations
import re

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from backend.config import CHAT_MODEL, anthropic_api_key
from backend.prompts import system_prompt

# Anthropic's server-side web search tool
# Claude decides when to call it, mirroring the OpenAI Responses
# `web_search` tool the previous chat model used.

WEB_SEARCH_TOOL = {"type": "web_search_20250305",
                   "name": "web_search"}

def chat() -> ChatAnthropic:
    llm = ChatAnthropic(
        model=CHAT_MODEL,
        temperature=0.4,
        api_key=anthropic_api_key(),
        max_tokens=1024,
    )

    return llm.bind_tools([WEB_SEARCH_TOOL])


def strip_dashes(text: str) -> str:
    """Replace em/en dashes with commas so replies read less machine-written.

    Plain hyphens are left alone (they belong in words like "plug-and-play" and
    names like "Walters-Storyk").
    """
    text = re.sub(r"\s*[—–]\s*", ", ", text)  # em/en dash -> comma
    text = re.sub(r",\s*([.!?,])", r"\1", text)          # tidy ", ." artifacts
    return text


def message_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, str):
                texts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        return "\n".join(t for t in texts if t).strip()
    return str(content)


def generate_reply(
    user_message: str,
    history: list[dict],
    context: str,
    lead_captured: bool = False,
    instruction: str = "",
) -> str:
    system = f"{system_prompt(lead_captured)}\n\nSTUDIO KNOWLEDGE CONTEXT:\n{context}"
    if instruction:
        system += f"\n\nFOR THIS REPLY: {instruction}"
    messages: list = [SystemMessage(content=system)]
    for turn in history[-6:]:
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["content"]))
        else:
            messages.append(AIMessage(content=turn["content"]))
    messages.append(HumanMessage(content=user_message))

    response = chat().invoke(messages)
    reply = message_text(response.content)
    if reply:
        return strip_dashes(reply)
    return (
        "Thanks for your message, I didn't catch that clearly. "
        "Could you rephrase, or tell me whether you're exploring our studios "
        "or if you need any help to contact us"
    )