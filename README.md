# Recall

A question-asking study buddy in a simple chat. Share notes in the message box.
Recall asks one question at a time, checks your answer against your material,
and gives hints before revealing an answer. Ask for an explanation, skip, or
say stop for a recap. It waits for material before starting practice.

Gemma runs on Google's servers; your laptop runs the small Python app. The tutor
is configured with instructions, not fine-tuned. Its responses can still make
mistakes; the prompt is guidance, not a guarantee of perfect grounding.

## Run locally

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open http://127.0.0.1:8501/ and share your study material in the message box. Enter sends;
Shift+Enter adds a line. **Start fresh** clears the conversation. If a reply fails,
**Try again** retries that message. Chat history is temporary and can reset on refresh.

## Configuration

The API key stays in `.streamlit/secrets.toml` under `GOOGLE_API_KEY`, or in that
environment variable. On a fresh checkout, copy `secrets.toml.example` to the
local secrets path. Do not commit the real key. Messages and conversation history
are sent to Google to generate replies. Provider quotas and terms apply.

## The active files

- `app.py`: greeting, messages, message box, and session state.
- `chat_engine.py`: checks and converts conversation roles for Gemma.
- `study_engine.py`: HTTPS request and readable service errors.
- `app_config.py`: private API key loading.
- `practice_settings.py`: name, greeting, and the tutor instructions.
- `styles.css`: light theme and purple accents.

For a hands-on change, edit the VOICE section of `TUTOR_INSTRUCTIONS` in
`practice_settings.py`. Start fresh and use the same notes to compare the tone.
The chat remains the entire interface: there are no setup forms or quiz modes.

## Fresh setup

Install Python 3.12+, then:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Checks

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Nine checks cover plain text replies, follow-up history, reset, error retries,
invalid input, missing keys, provider output, and safe quota errors.
`check_live.py` sends five real requests with public queue/stack notes so you
can inspect missing-context handling, a question, a hint, and a recap.
`package_source.py` creates a source archive without the real key or environment.
Public hosting and challenge submission remain separate steps. See `DEPLOY.md`.

## License

The app code is MIT licensed. Gemma and the hosted API have their own terms.
