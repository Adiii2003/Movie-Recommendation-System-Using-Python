import os
import pickle
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# --- Setup ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    st.error("TMDB_API_KEY missing. Create .env with TMDB_API_KEY=your_key")
    st.stop()

BASE_DIR = os.path.dirname(__file__)
MOVIE_LIST_PKL = os.path.join(BASE_DIR, "movie_list.pkl")
SIMILARITY_PKL = os.path.join(BASE_DIR, "similarity.pkl")

# --- Load Artifacts ---
movies = pickle.load(open(MOVIE_LIST_PKL, "rb"))   # DataFrame with columns: movie_id, title
similarity = pickle.load(open(SIMILARITY_PKL, "rb"))

# --- TMDB Poster Helper ---
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# --- Recommender ---
def recommend(movie_title: str, k: int = 5):
    # exact title match (you can improve with fuzzy matching later)
    idx = movies.index[movies["title"] == movie_title]
    if len(idx) == 0:
        return []
    i = idx[0]
    distances = similarity[i]
    # sort by similarity score, skip the first (itself)
    top = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:k+1]
    results = []
    for j, _ in top:
        mid = int(movies.iloc[j].movie_id)
        title = movies.iloc[j].title
        results.append({"title": title, "poster": fetch_poster(mid)})
    return results

# --- UI ---
st.title("🎬 Movie Recommender System")
st.caption("Select a movie to get top recommendations with posters.")

selected = st.selectbox("Pick a movie", movies["title"].values)

if st.button("Show Recommendations"):
    recs = recommend(selected, k=6)
    if not recs:
        st.warning("No recommendations found.")
    else:
        cols = st.columns(6)
        for col, rec in zip(cols, recs):
            with col:
                st.image(rec["poster"])
                st.write(rec["title"])
