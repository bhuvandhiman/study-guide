"""Load private configuration without exposing credentials in the page."""

import os
import tomllib
from pathlib import Path

import streamlit as st


def get_api_key():
    key = os.environ.get("GOOGLE_API_KEY", "")
    local_secrets = Path(__file__).parent / ".streamlit" / "secrets.toml"
    if not key and local_secrets.exists():
        try:
            key = tomllib.loads(local_secrets.read_text(encoding="utf-8")).get("GOOGLE_API_KEY", "")
        except (OSError, ValueError):
            return ""
    if not key:
        try:
            key = st.secrets.get("GOOGLE_API_KEY", "")
        except FileNotFoundError:
            pass
    if not isinstance(key, str) or key.strip() == "replace-with-your-key":
        return ""
    return key.strip()
