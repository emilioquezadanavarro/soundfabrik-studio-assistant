from backend.config import MAX_MESSAGE_CHARS, MAX_TURNS_PER_SESSION
from backend.pipeline import SessionState, handle_turn
from backend.prompts import MESSAGE_TOO_LONG_REPLY, RATE_LIMIT_REPLY


def test_handle_turn_rejects_message_over_max_length():
    result = handle_turn("x" * (MAX_MESSAGE_CHARS + 1), [])
    assert result.reply == MESSAGE_TOO_LONG_REPLY


def test_handle_turn_rate_limits_after_max_turns():
    state = SessionState(turn_count=MAX_TURNS_PER_SESSION)
    result = handle_turn("Hi again", [], state=state)
    assert result.reply == RATE_LIMIT_REPLY
