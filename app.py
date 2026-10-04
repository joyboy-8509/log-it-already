import streamlit as st
import os
import requests
from bs4 import BeautifulSoup
import re

st.set_page_config(page_title="Log It Already", layout="centered")

# Inject Nothing OS Aesthetic CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

.stApp {
    background-color: #1B1D1F;
    color: #F1F1F1;
}
h1, h2, h3, p, div, label, span {
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Titles */
.main-title {
    font-size: 3.8rem;
    font-weight: 700;
    color: #F1F1F1;
    margin-bottom: 5px;
    letter-spacing: -1.5px;
}
.subtitle {
    color: #999;
    font-size: 1.1rem;
    margin-bottom: 2.5rem;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 600;
    color: #F1F1F1;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #333;
    padding-bottom: 0.5rem;
}

/* Output Layout Typography */
.movie-title {
    font-size: 2.8rem;
    font-weight: 700;
    margin-top: 0px;
    line-height: 1.1;
    color: #F1F1F1;
}
.about-heading {
    font-size: 1.1rem;
    font-weight: 600;
    color: #D71921; /* Nothing OS Red */
    margin-top: 1.8rem;
    margin-bottom: 0.5rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.about-text {
    font-size: 1.15rem;
    line-height: 1.6;
    color: #e0e0e0;
}

/* Custom Inputs */
.stTextInput input {
    background-color: #111 !important;
    color: #F1F1F1 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 14px 16px !important;
    font-size: 1.05rem !important;
}
.stTextInput input:focus {
    border: 1px solid #D71921 !important;
    box-shadow: none !important;
}

/* Custom Button */
.stButton>button {
    background-color: #F1F1F1 !important;
    color: #1B1D1F !important;
    border-radius: 30px !important;
    border: none !important;
    padding: 10px 24px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.2s ease;
    margin-top: 1.5rem;
    width: 100%; /* Makes button fill the container nicely */
}
.stButton>button:hover {
    background-color: #D71921 !important;
    color: #F1F1F1 !important;
}

/* Alerts / Banners */
.stAlert {
    background-color: #111 !important;
    color: #F1F1F1 !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Log It Already</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>For the cinephile with 500 movies in their watchlist and 45 minutes of decision paralysis.</div>", unsafe_allow_html=True)

# Load the API key
api_key = ""
key_file_path = "saved_key.txt"

if "OLLAMA_API_KEY" in st.secrets:
    api_key = st.secrets["OLLAMA_API_KEY"]
elif os.path.exists(key_file_path):
    with open(key_file_path, "r") as f:
        api_key = f.read().strip()
else:
    api_key = os.environ.get("OLLAMA_API_KEY", "")

# First-time setup screen for friends who don't have the key configured
if not api_key:
    st.markdown("<div class='section-title'>First-Time Setup</div>", unsafe_allow_html=True)
    st.markdown("<div class='about-text'>Welcome! To use Log It Already, you need an Ollama API key. Paste it below to save it securely to your machine. You only need to do this once!</div><br>", unsafe_allow_html=True)
    
    user_key = st.text_input("Ollama API Key:", type="password", placeholder="Paste your API key here...")
    if st.button("Save Key & Start"):
        if user_key:
            with open(key_file_path, "w") as f:
                f.write(user_key.strip())
            st.rerun()
    st.stop()  # Halt rendering the rest of the app until the key is provided

st.markdown("<div class='section-title'>Your Watchlist (Optional)</div>", unsafe_allow_html=True)
url = st.text_input(
    "Paste a Letterboxd List or Watchlist URL (Optional):", 
    placeholder="https://letterboxd.com/username/watchlist/ (Leave blank for global trends)", 
    label_visibility="collapsed"
)

st.markdown("<div class='section-title'>Your Vibe</div>", unsafe_allow_html=True)
mood = st.text_input(
    "What's your mood tonight?",
    placeholder="e.g., Brain fried from work, or 'bhai aaj kuch rula dene wali sci-fi bata'",
    label_visibility="collapsed"
)

if st.button("Pick My Movie", type="primary"):
    if not api_key:
        st.error("Server Configuration Error: API key is missing from the backend.")
    elif not mood:
        st.warning("Please tell us your mood so we can pick a movie!")
    else:
        movies_dict = {}
        if url:
            with st.spinner("Scraping Letterboxd..."):
                try:
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    res = requests.get(url, headers=headers, timeout=30)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    
                    for poster in soup.find_all('div', class_='film-poster'):
                        img = poster.find('img')
                        if img and img.has_attr('alt'):
                            title = img['alt'].strip()
                            src = img.get('src') or img.get('data-src') or "https://via.placeholder.com/300x450?text=Poster"
                            movies_dict[title] = src
                    
                    if not movies_dict:
                        st.warning("Could not find any movies on that link. Suggesting a trending movie instead!")
                except Exception as e:
                    st.warning("Could not load the list, suggesting a trending movie instead!")

        if movies_dict:
            watchlist_text = ", ".join(movies_dict.keys())
            prompt = f"""You are an expert film curator. A user has the following movies in their Letterboxd watchlist:
            
            {watchlist_text}
            
            Their current mood is: "{mood}"
            (Note: The user's mood might be written in Hinglish - a mix of Hindi and English. Please interpret it accurately. If their mood is in Hinglish, feel free to write the ABOUT section in a natural, conversational Hinglish tone as well).
            
            Based ONLY on the movies in their watchlist, pick the absolute best movie for them to watch right now. 
            Format your response EXACTLY like this and include nothing else:
            
            TITLE: [Exact Movie Title]
            ABOUT: [Explain why it fits their specific mood and what they can expect]
            """
        else:
            prompt = f"""You are an expert film curator. A user is looking for a movie recommendation.
            
            Their current mood is: "{mood}"
            (Note: The user's mood might be written in Hinglish - a mix of Hindi and English. Please interpret it accurately. If their mood is in Hinglish, feel free to write the ABOUT section in a natural, conversational Hinglish tone as well).
            
            Pick the absolute best, highly acclaimed or currently trending movie for them to watch right now. 
            Format your response EXACTLY like this and include nothing else:
            
            TITLE: [Exact Movie Title]
            ABOUT: [Explain why it fits their specific mood and what they can expect]
            """
            
        with st.spinner("Analyzing your vibe to find the perfect movie..."):
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "gemma4:31b", 
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                }
                
                response = requests.post("https://ollama.com/api/chat", headers=headers, json=data)
                response.raise_for_status()
                
                result = response.json()
                raw_text = result['message']['content']
                
                title_match = re.search(r'TITLE:\s*(.*?)(?:\n|$)', raw_text, re.IGNORECASE)
                about_match = re.search(r'ABOUT:\s*(.*)', raw_text, re.DOTALL | re.IGNORECASE)
                
                suggested_title = title_match.group(1).strip().replace("*", "").replace('"', "") if title_match else "Movie Pick"
                about_text = about_match.group(1).strip() if about_match else raw_text
                
                # Try to exact-match the scraped list if it exists
                if movies_dict:
                    for m_title in movies_dict.keys():
                        if suggested_title.lower() in m_title.lower() or m_title.lower() in suggested_title.lower():
                            suggested_title = m_title
                            break
                
                poster_url = "https://via.placeholder.com/300x450?text=No+Poster"
                slug = re.sub(r'[^a-z0-9]+', '-', suggested_title.lower()).strip('-')
                
                try:
                    movie_res = requests.get(f"https://letterboxd.com/film/{slug}/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                    if movie_res.status_code == 200:
                        movie_soup = BeautifulSoup(movie_res.text, 'html.parser')
                        
                        script_tag = movie_soup.find('script', type='application/ld+json')
                        if script_tag:
                            match = re.search(r'"image"\s*:\s*"([^"]+)"', script_tag.string)
                            if match:
                                poster_url = match.group(1)
                        
                        if poster_url == "https://via.placeholder.com/300x450?text=No+Poster":
                            og_image = movie_soup.find('meta', property='og:image')
                            if og_image and og_image.has_attr('content'):
                                poster_url = og_image['content']
                except:
                    pass
                
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown(f'<img src="{poster_url}" style="width:100%; border-radius:20px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown(f'''
                        <div class="movie-title">{suggested_title}</div>
                        <div class="about-heading">about movie</div>
                        <div class="about-text">{about_text}</div>
                    ''', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error("Could not connect to the AI model.")
                st.error(f"Details: {str(e)}")
