import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
MOVIES_CSV = os.path.join(BASE_DIR, "data", "tmdb_5000_movies.csv")
CREDITS_CSV = os.path.join(BASE_DIR, "data", "tmdb_5000_credits.csv")
MOVIE_LIST_PKL = os.path.join(BASE_DIR, "movie_list.pkl")
SIMILARITY_PKL = os.path.join(BASE_DIR, "similarity.pkl")

# Helpers to parse stringified JSON
def parse_name_list(x):
    try:
        return [i["name"] for i in ast.literal_eval(x)]
    except Exception:
        return []

def parse_top_cast(x, topn=3):
    try:
        names = [i["name"] for i in ast.literal_eval(x)]
        return names[:topn]
    except Exception:
        return []

def get_director(x):
    try:
        for crew in ast.literal_eval(x):
            if crew.get("job") == "Director":
                return [crew.get("name")]
    except Exception:
        pass
    return []

def clean_tokens(tokens):
    # lowercase + remove internal spaces in multi-word names (e.g., "Sam Worthington" -> "samworthington")
    return [t.replace(" ", "").lower() for t in tokens]

# Load
movies = pd.read_csv(MOVIES_CSV)
credits = pd.read_csv(CREDITS_CSV)

# Merge on title
df = movies.merge(credits, left_on="title", right_on="title")

# Keep important cols
df = df[["id", "title", "overview", "genres", "keywords", "cast", "crew"]]

# Fill NaN
df["overview"] = df["overview"].fillna("")
df["genres"] = df["genres"].fillna("[]")
df["keywords"] = df["keywords"].fillna("[]")
df["cast"] = df["cast"].fillna("[]")
df["crew"] = df["crew"].fillna("[]")

# Build tag field
df["genres"] = df["genres"].apply(parse_name_list)
df["keywords"] = df["keywords"].apply(parse_name_list)
df["cast"] = df["cast"].apply(lambda x: parse_top_cast(x, topn=3))
df["crew"] = df["crew"].apply(get_director)

df["genres"] = df["genres"].apply(clean_tokens)
df["keywords"] = df["keywords"].apply(clean_tokens)
df["cast"] = df["cast"].apply(clean_tokens)
df["crew"] = df["crew"].apply(clean_tokens)

df["overview_tokens"] = df["overview"].apply(lambda x: x.lower().split())

df["tags"] = df["overview_tokens"] + df["genres"] + df["keywords"] + df["cast"] + df["crew"]
df["tags"] = df["tags"].apply(lambda x: " ".join(x))

# Vectorize + similarity
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(df["tags"]).toarray()
similarity = cosine_similarity(vectors)

# Save artifacts
# We'll keep only what's needed by the app: movie_id and title (index alignment matters!)
movie_list = df[["id", "title"]].rename(columns={"id": "movie_id"}).reset_index(drop=True)

with open(MOVIE_LIST_PKL, "wb") as f:
    pickle.dump(movie_list, f)

with open(SIMILARITY_PKL, "wb") as f:
    pickle.dump(similarity, f)

print("Artifacts created:")
print(f" - {MOVIE_LIST_PKL}")
print(f" - {SIMILARITY_PKL}")
