# my-assistant
Personal Assistant chatbot (Streamlit) — local JSON memory

## Features
- Streamlit chat UI
- Uses OpenAI Chat API (configurable model, default: gpt-4o)
- Local JSON memory stored in `memory.json`
- Save quick memories, view and clear memory

## Setup (Local or Streamlit Cloud)
1. Clone the repo or upload files to Streamlit Cloud.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key:
   - Locally: set `OPENAI_API_KEY` env variable, or create a `.env` file.
   - Streamlit Cloud: go to App → Settings → Secrets and add `OPENAI_API_KEY`.
4. Run locally:
   ```bash
   streamlit run app.py
   ```
5. Or deploy on Streamlit Cloud (connect GitHub repo, set main file `app.py`, add secret `OPENAI_API_KEY`).

## Notes
- Memory is stored in `memory.json` in the app folder. For long-term persistence use Google Drive mounting or a DB.
- To change model, edit `OPENAI_MODEL` env var or change in Streamlit sidebar.
