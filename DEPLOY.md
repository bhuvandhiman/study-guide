# Share the app on Streamlit Community Cloud

The app runs locally and the Gemma connection has passed a live sample check.
These are the remaining steps to give a friend a public link.

## 1. Put the source in a GitHub repository

Create a repository in your GitHub account. Upload the source from
`dist/recall-source.zip` after extracting it. Include its `.streamlit/config.toml`
file. The archive excludes `.streamlit/secrets.toml`, `.venv`, and cache files.
Commit the source to your chosen branch.

## 2. Deploy

Open https://share.streamlit.io and connect your GitHub account. Choose Create app,
select the repository and branch, and set the main file path to `app.py`.
In Advanced settings choose Python 3.12 or later.

Add this in the deployment's private Secrets settings, with your actual key:

```toml
GOOGLE_API_KEY = "your-key-here"
```

Click Deploy. The platform installs `requirements.txt` and starts the page.
The public app calls Google's hosted Gemma; no GPU runs in the Streamlit host.

## 3. Check the public link

Share notes and answer the first question. Try a wrong answer, ask for a hint,
then ask for a recap. Check that Start fresh clears the conversation.

The friend's requests consume the Google project's quota. Sessions are temporary;
chat history can reset on refresh. Messages and conversation history are
processed by Google, and its provider data terms apply.

## Challenge entry

The intended category is Best Use of Gemma: Gemma provides the chat replies.
For an entry, use the official DEV template and #hf26challenge.
Include the demo link, code link, one real friend's experience, and an honest
explanation of why the open model matters. The app is hosted and requires internet.
Neither the public deployment nor the DEV submission has been made yet.

Official docs:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app
