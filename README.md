![My Current Top 4](assets/top4.png)
### My Current Top 4

# 🍿 Log It Already (Hacktoberfest Weekend Challenge: Build for a Friend)

For the cinephile with 500 movies in their watchlist and 45 minutes of decision paralysis. 
"Log It Already" is a minimalist, AI-powered movie recommender built with a clean, high-contrast aesthetic. It scans your Letterboxd watchlist and uses AI to pick the absolute best movie for your current mood.

## Features
* **Letterboxd Integration:** Automatically scrapes your public watchlist.
* **Vibe Check:** Tell the AI exactly what you're in the mood for.
* **Minimalist UI:** Clean, high-contrast, distraction-free design.
* **Smart Fallback:** Don't have a watchlist? Leave it blank and the AI will recommend a global trending movie based on your mood.

## How to Run

### Prerequisites
1. Python 3.9+
2. [Ollama](https://ollama.com/) (If running local models) or an Ollama Cloud API Key.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/joyboy-8509/log-it-already.git
   cd log-it-already
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Ollama API key as an environment variable (or safely save it in a `saved_key.txt` file in the root directory):
   ```bash
   # On Windows (PowerShell)
   $env:OLLAMA_API_KEY="your-api-key-here"
   
   # On Mac/Linux
   export OLLAMA_API_KEY="your-api-key-here"
   ```

### Execution
Run the app using Streamlit:
```bash
streamlit run app.py
```
