"""Public material for manually checking the tutor with five real API requests."""

from app_config import get_api_key
from chat_engine import reply_to_chat
from study_engine import StudyError

PROMPTS = [
    "Hi, can you quiz me?",
    "My notes: A queue follows first-in, first-out (FIFO). A stack follows last-in, first-out (LIFO). Start with the queue.",
    "A queue is last-in, first-out.",
    "First-in, first-out: the item added first comes out first.",
    "Stop and give me a short recap.",
]


def main():
    messages = []
    try:
        key = get_api_key()
        for number, prompt in enumerate(PROMPTS, 1):
            messages.append({"role": "user", "content": prompt})
            reply = reply_to_chat(messages, key)
            messages.append({"role": "assistant", "content": reply})
            print(f"Turn {number}: {reply}\n")
            if reply.count("?") > 1:
                raise StudyError("More than one question was returned. Review the tutor instructions.")
        print("Live requests completed. Review the replies for grounding, hints, and an honest recap.")
    except StudyError as error:
        print(f"LIVE CHECK: {error}")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
