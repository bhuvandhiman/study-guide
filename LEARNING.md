# How Recall works

The interface is a chat. The tutor behavior comes from `TUTOR_INSTRUCTIONS` in
`practice_settings.py`. We send those instructions with the conversation on
each request. This is prompt customization of hosted Gemma, not fine-tuning.

1. `app.py` displays the welcome, conversation, and one message box.
2. `chat_engine.py` validates messages, adds the tutor instructions to a separate
   text part, and maps assistant messages to the provider's model role.
3. `study_engine.py` makes the HTTPS request and extracts the reply text.
4. `st.session_state.messages` remembers the conversation until it is cleared or
   the browser session resets. The API key stays on the Python server.

The intended flow is notes → one question → your attempt → feedback or hint.
A correct answer moves the conversation forward. A mistaken answer gets another
attempt. An explicit request can reveal an explanation, skip, or end practice.
Questions should stay grounded in the notes, but model behavior still needs review.

Try changing the VOICE section of the tutor instructions. Start fresh, reuse the
same notes, and compare how helpful the hints feel. Nine automated checks cover
transport, history, instruction injection, retry, and reset. `check_live.py` is a
separate, real-API behavior check whose replies should be reviewed by a person.
