# assistant.py
import os
import json
import time
from typing import List, Dict
import openai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY

MEMORY_FILE = "memory.json"

def load_memory() -> List[Dict]:
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_memory(mem: List[Dict]):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

def add_memory(text: str, tag: str = ""):
    mem = load_memory()
    mem.append({"text": text, "tag": tag, "ts": int(time.time())})
    save_memory(mem)

def clear_memory():
    save_memory([])

def build_system_prompt(mem: List[Dict]) -> str:
    if not mem:
        return "You are a helpful personal assistant. Keep answers concise and friendly."
    last = mem[-10:]
    mem_text = "\n".join([f"- {m.get('text')} ({m.get('tag','')})" for m in reversed(last)])
    prompt = (
        "You are a helpful and polite personal assistant. Use the user's stored memory to personalize responses.\n\n"
        "User memory (most recent first):\n"
        f"{mem_text}\n\n"
        "When responding, you MAY reference the memory if relevant. Keep answers concise."
    )
    return prompt

def chat_with_assistant(user_message: str, model: str = DEFAULT_MODEL, temperature: float = 0.3) -> str:
    mem = load_memory()
    system_msg = build_system_prompt(mem)

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_message}
    ]

    try:
        resp = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=500,
        )
        reply = resp["choices"][0]["message"]["content"].strip()
        return reply
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
