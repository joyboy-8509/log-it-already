# Hacktoberfest 2026: Build for a Friend

**Challenge:** Hacktoberfest Weekend Challenge (Oct 2 - Oct 5)
**Theme:** Build for a Friend
**Requirement:** Open-Source AI at its core

## Project: Letterboxd Backlog Buster
A standalone Web App built with Streamlit and Gemma 2 (9B) via Hugging Face.

### Why Open Matters (For your DEV post):
A cinephile's watchlist and viewing moods are deeply personal reflections of their mental state. Passing that data to a closed model means Big Tech is profiling their entertainment preferences to sell ads. Using an open-weight model like Gemma keeps their cinematic taste and personal moods completely private.

### Files in this folder:
* `app.py`: The Streamlit application we wrote together.
* `chat_transcript.jsonl`: The raw log of our entire brainstorming session (you can optionally embed snippets of this in your DEV post using DevRelay to show your process!).

### How to Run:
1. `pip install streamlit huggingface_hub`
2. `streamlit run app.py`
