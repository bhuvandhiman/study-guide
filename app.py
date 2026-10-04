"""A question-asking study buddy in one simple conversation."""

from html import escape
from pathlib import Path

import streamlit as st

from app_config import get_api_key
from chat_engine import MAX_MESSAGE, reply_to_chat
from practice_settings import APP_DESCRIPTION, APP_SUBTITLE, APP_TITLE
from study_engine import StudyError

st.set_page_config(page_title=APP_TITLE, page_icon="✦", layout="centered")
st.html(f"<style>{Path(__file__).with_name('styles.css').read_text(encoding='utf-8')}</style>")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("pending_reply", False)
st.session_state.setdefault("chat_error", "")


def clear_chat():
    st.session_state.messages = []
    st.session_state.pending_reply = False
    st.session_state.chat_error = ""


def retry_reply():
    st.session_state.pending_reply = True
    st.session_state.chat_error = ""


with st.container(key="chat_header", horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
    st.html(f'<div class="chat-brand"><span class="brand-mark" aria-hidden="true">r</span><div>{escape(APP_TITLE)}<small>YOUR STUDY BUDDY</small></div></div>')
    if st.session_state.messages:
        st.button("Start fresh", icon=":material/refresh:", key="new_chat", help="Clear these notes and start a new conversation",
                  on_click=clear_chat)

if not st.session_state.messages:
    headline = escape(APP_SUBTITLE).replace("\n", "<br>")
    st.html(f'''<div class="welcome"><div class="orb" aria-hidden="true"><span>?</span></div>
        <p class="eyebrow">LET'S SEE WHAT STICKS</p><h1>{headline}</h1>
        <p class="welcome-description">{escape(APP_DESCRIPTION)}</p>
        <p class="welcome-note">One question at a time. Room to get it wrong.</p></div>''')

key = get_api_key()
if not key:
    st.error("Gemma isn't connected yet. Add your Google API key to the local secrets file.")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=":material/auto_awesome:" if message["role"] == "assistant" else ":material/person:"):
        st.markdown(message["content"])

placeholder = "Share your notes to get started…" if not st.session_state.messages else "Your answer, a hint request, or more notes…"
prompt = st.chat_input(placeholder, key="message_input", max_chars=MAX_MESSAGE,
                       disabled=not key or bool(st.session_state.chat_error) or st.session_state.pending_reply)
if prompt and prompt.strip():
    st.session_state.messages.append({"role": "user", "content": prompt.strip()})
    st.session_state.pending_reply = True
    st.rerun()

if st.session_state.pending_reply:
    with st.chat_message("assistant", avatar=":material/auto_awesome:"):
        try:
            with st.spinner("Thinking it through…"):
                reply = reply_to_chat(st.session_state.messages, key)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.pending_reply = False
            st.rerun()
        except StudyError as error:
            st.session_state.pending_reply = False
            st.session_state.chat_error = str(error)

if st.session_state.chat_error:
    st.error(st.session_state.chat_error)
    st.button("Try again", key="retry_reply", on_click=retry_reply)
