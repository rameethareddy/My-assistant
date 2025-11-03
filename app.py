# app.py - Streamlit Personal Assistant (local-json memory)
import streamlit as st
import os
from assistant import load_memory, add_memory, clear_memory, chat_with_assistant, MEMORY_FILE
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Personal Assistant", layout="wide")
st.title("🧠 Personal Assistant — Streamlit (local-json memory)")

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    st.markdown("""Set your OpenAI API key as a Streamlit Secret named `OPENAI_API_KEY` or paste it below (session only).""")
    api_key_input = st.text_input("OpenAI API Key (optional)", type="password")
    model = st.text_input("Model", value=os.getenv("OPENAI_MODEL", "gpt-4o"))
    temp = st.slider("Temperature", 0.0, 1.0, 0.3)
    if api_key_input:
        os.environ["OPENAI_API_KEY"] = api_key_input
        st.success("API key set for this session (not persisted).")

    st.markdown("---")
    st.markdown("Memory management:")
    if st.button("Clear memory (delete all)"):
        clear_memory()
        st.success("Memory cleared.")

mem = load_memory()

st.subheader("Memory (basic)")
col1, col2 = st.columns([3,1])
with col1:
    if mem:
        for i,m in enumerate(reversed(mem)):
            st.markdown(f"**{len(mem)-i}.** {m['text']}  \n_tag:_ {m.get('tag','')}")
    else:
        st.info("No memories yet. Add something below.")

with col2:
    st.write("")
    if st.button("Reload memory"):
        st.experimental_rerun()

st.markdown("---")
st.subheader("Add memory (quick)")
with st.form("mem_form", clear_on_submit=True):
    mem_text = st.text_area("Remember this for me:", help="Short sentence about user preference, facts, etc.")
    mem_tag = st.text_input("Tag (optional): e.g., 'preference', 'birthday'")
    submitted = st.form_submit_button("Save memory")
    if submitted:
        if mem_text.strip():
            add_memory(mem_text.strip(), mem_tag.strip())
            st.success("Memory saved.")
            st.experimental_rerun()
        else:
            st.error("Enter some text to save.")

st.markdown("---")
st.subheader("Chat with your assistant")
if "history" not in st.session_state:
    st.session_state.history = []

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("You:", placeholder="Ask something, or say 'remember ...' to add a memory")
    send = st.form_submit_button("Send")
    if send and user_input.strip():
        lowered = user_input.lower()
        if lowered.startswith("remember ") or lowered.startswith("remember that ") or "remind" in lowered[:12]:
            add_memory(user_input.strip(), tag="user-note")
            st.success("Saved to memory.")
            st.session_state.history.append(("user", user_input))
        else:
            st.session_state.history.append(("user", user_input))
            reply = chat_with_assistant(user_input, model=model, temperature=float(temp))
            st.session_state.history.append(("assistant", reply))

for role, text in st.session_state.history[::-1]:
    if role == "user":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Assistant:** {text}")

st.markdown("---")
st.markdown("Tip: add memories with the 'Add memory' box or by typing 'Remember ...' at the start of your message.")
