"""Give Gemma the tutor instructions and conversation, then return its reply."""

from study_engine import StudyError, request_text
from practice_settings import TUTOR_INSTRUCTIONS

MAX_MESSAGE = 10000
MAX_CONVERSATION = 60000


def reply_to_chat(messages, api_key):
    if not isinstance(messages, list) or not messages:
        raise StudyError("Write a message first.")
    contents = []
    total = 0
    for message in messages:
        if not isinstance(message, dict) or message.get("role") not in ("user", "assistant"):
            raise StudyError("This conversation could not be read. Start a new chat.")
        text = message.get("content")
        if not isinstance(text, str) or not text.strip():
            raise StudyError("Write a message first.")
        if message["role"] == "user" and len(text) > MAX_MESSAGE:
            raise StudyError("Please keep each message under 10,000 characters.")
        total += len(text)
        contents.append({"role": "model" if message["role"] == "assistant" else "user",
                         "parts": [{"text": text}]})
    if total > MAX_CONVERSATION:
        raise StudyError("This conversation is getting long. Start a new chat to continue.")
    if messages[-1]["role"] != "user":
        raise StudyError("Write a message before asking for a reply.")
    # Gemma receives the tutor role as a separate text part of the first turn.
    # Build new dictionaries so instructions never leak into the visible history.
    contents[0]["parts"].insert(0, {"text": TUTOR_INSTRUCTIONS})
    return request_text(api_key, contents=contents)
