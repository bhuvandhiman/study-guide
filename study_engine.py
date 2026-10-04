"""Hosted Gemma HTTP requests and readable service errors."""

import json
import ssl
import urllib.error
import urllib.request

import certifi

MODEL = "gemma-4-26b-a4b-it"


class StudyError(Exception):
    """A short, safe message we can show in the page."""


def request_text(api_key, *, contents):
    """Send one request to hosted Gemma. The key stays on the Python server."""
    if not isinstance(api_key, str) or not api_key.strip():
        raise StudyError("Add your Google API key before using Gemma.")
    body = {
        "contents": contents,
        "generationConfig": {
            "temperature": 0.3, "maxOutputTokens": 4096,
            "thinkingConfig": {"thinkingLevel": "minimal"},
        },
    }
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        with urllib.request.urlopen(request, timeout=60, context=context) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        messages = {
            400: "Google rejected the request. Check model access and try a shorter message.",
            401: "The API key was not accepted. Check your local secrets file.",
            403: "Your key or Google project cannot access this model. Check AI Studio.",
            404: "This Gemma model is unavailable for your project. Check the model ID.",
            429: "Your API quota was reached. Wait before trying again; check AI Studio limits.",
        }
        raise StudyError(messages.get(error.code, "The model service is unavailable. Try again later.")) from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise StudyError("Could not reach the model. Check your internet connection and try again.") from None
    except ValueError:
        raise StudyError("The model service returned unreadable data. Please try again.") from None
    try:
        if not isinstance(data, dict):
            raise ValueError("Response is not an object")
        candidate = data["candidates"][0]
        if not isinstance(candidate, dict):
            raise ValueError("Invalid response candidate")
        if candidate.get("finishReason") == "MAX_TOKENS":
            raise StudyError("The model response was cut off. Try asking for a shorter reply.")
        parts = data["candidates"][0]["content"]["parts"]
        if not isinstance(parts, list) or any(not isinstance(part, dict) for part in parts):
            raise ValueError("Invalid response parts")
        text = "".join(part.get("text", "") for part in parts if not part.get("thought"))
        text = text.strip()
        if not text:
            raise ValueError("Empty response")
        return text
    except (KeyError, IndexError, TypeError, ValueError):
        raise StudyError("The model returned an unexpected format. Please try again.") from None

