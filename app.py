import os
import pickle
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import gdown
import numpy as np
# --- Setup ---

load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY")

if not TMDB_KEY:
    st.error("TMDB_API_KEY missing. Create .env with TMDB_API_KEY=your_key")
    st.stop()

# --- Streamlit Config ---
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# --- File Paths and Google Drive Setup ---

BASE_DIR = os.path.dirname(__file__)
MOVIE_LIST_PKL = os.path.join(BASE_DIR, "movie_list.pkl")
SIMILARITY_PKL = os.path.join(BASE_DIR, "similarity.pkl")

# Google Drive file id (from your link)
# Prefer to put this into Streamlit Secrets as GDRIVE_FILE_ID
DEFAULT_FILE_ID = "1_8D6AsRiUuVCdX3B17QsnHmFDrYW83Me"
GDRIVE_FILE_ID = st.secrets.get("GDRIVE_FILE_ID", DEFAULT_FILE_ID)
DRIVE_URL = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"



# --- Load Artifacts with caching ---
@st.cache_data(show_spinner=False)
def load_movie_list(path=MOVIE_LIST_PKL):
    if not os.path.exists(path):
        st.error(f"Missing {path}. Make sure movie_list.pkl is present in the repo.")
        st.stop()
    with open(path, "rb") as f:
        return pickle.load(f)

@st.cache_resource(show_spinner=False)
def load_similarity(path=SIMILARITY_PKL, drive_url=DRIVE_URL):
    # Download only if not present
    if not os.path.exists(path):
        # st.info("Downloading similarity matrix (first run)...")
        # gdown will follow the Drive confirm page for large files
        gdown.download(drive_url, path, quiet=False)
        if not os.path.exists(path):
            st.error("Failed to download similarity.pkl from Google Drive. Check GDRIVE_FILE_ID and sharing settings.")
            st.stop()
    with open(path, "rb") as f:
        return pickle.load(f)

# Load data
movies = load_movie_list()       # expected: DataFrame with columns movie_id, title
similarity = load_similarity()   # expected: square matrix (n_movies x n_movies)

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








# import os
# import pickle
# import requests
# import pandas as pd
# import streamlit as st
# from dotenv import load_dotenv

# # --- Setup ---

# load_dotenv()

# TMDB_KEY = os.getenv("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY")

# if not TMDB_KEY:
#     st.error("TMDB_API_KEY missing. Create .env with TMDB_API_KEY=your_key")
#     st.stop()


# # --- Streamlit Config ---
# st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")


# BASE_DIR = os.path.dirname(__file__)
# MOVIE_LIST_PKL = os.path.join(BASE_DIR, "movie_list.pkl")
# SIMILARITY_PKL = os.path.join(BASE_DIR, "similarity.pkl")

# # --- Load Artifacts ---
# movies = pickle.load(open(MOVIE_LIST_PKL, "rb"))   # DataFrame with columns: movie_id, title
# similarity = pickle.load(open(SIMILARITY_PKL, "rb"))

# # --- TMDB Poster Helper ---
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# # --- Recommender ---
# def recommend(movie_title: str, k: int = 5):
#     # exact title match (you can improve with fuzzy matching later)
#     idx = movies.index[movies["title"] == movie_title]
#     if len(idx) == 0:
#         return []
#     i = idx[0]
#     distances = similarity[i]
#     # sort by similarity score, skip the first (itself)
#     top = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:k+1]
#     results = []
#     for j, _ in top:
#         mid = int(movies.iloc[j].movie_id)
#         title = movies.iloc[j].title
#         results.append({"title": title, "poster": fetch_poster(mid)})
#     return results

# # --- UI ---
# st.title("🎬 Movie Recommender System")
# st.caption("Select a movie to get top recommendations with posters.")

# selected = st.selectbox("Pick a movie", movies["title"].values)

# if st.button("Show Recommendations"):
#     recs = recommend(selected, k=6)
#     if not recs:
#         st.warning("No recommendations found.")
#     else:
#         cols = st.columns(6)
#         for col, rec in zip(cols, recs):
#             with col:
#                 st.image(rec["poster"])
#                 st.write(rec["title"])