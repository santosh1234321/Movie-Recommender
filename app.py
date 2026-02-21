import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

# 1. Setup a robust Session to handle connection resets (Error 10054)
def create_session():
    session = requests.Session()
    # Retry strategy: wait between attempts if the server is busy
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    return session

session = create_session()

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    try:
        # Reusing the session prevents the "Forcibly Closed" error
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        # Fallback to a clean placeholder if the API fails
        return "https://via.placeholder.com/500x750?text=Poster+Not+Available"
    return "https://via.placeholder.com/500x750?text=Poster+Not+Available"

# 2. Load the Data
try:
    movies = pickle.load(open("movies_list.pkl", 'rb'))
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    movies_list = movies['title'].values
except FileNotFoundError:
    st.error("Missing Data: Please run your recommender.py script first to generate pickle files.")
    st.stop()

# 3. UI Configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Search or select a movie from the database:",
    movies_list
)

# 4. Recommendation Logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    names = []
    posters = []
    
    # We fetch 5 movies, skipping index 0 (the movie itself)
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        names.append(movies.iloc[i[0]].title)
        
        # Human-like delay to avoid getting blocked by TMDB
        time.sleep(0.3) 
        posters.append(fetch_poster(movie_id))
        
    return names, posters

# 5. Display Interface
if st.button("Get Recommendations"):
    with st.spinner('Analyzing patterns and fetching posters...'):
        names, posters = recommend(selected_movie)
        
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.markdown(f"**{names[i]}**")
                st.image(posters[i], use_container_width=True)
