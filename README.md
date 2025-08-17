# Movie-Recommendation-System-Using-Python

**A simple, fast movie recommendation web app built with Python and Streamlit.**  
Uses content-based filtering (TF-IDF on movie metadata) and a precomputed similarity matrix to recommend similar movies based on the selected title.

---

## 🚀 Features
- Content-based recommendations using movie metadata (title, overview, genres, etc.)
- Fast lookup via a precomputed similarity matrix (`similarity.pkl`)
- Lightweight Streamlit UI for interactive usage
- Easy to extend with more data or different similarity measures

---

## 📁 Project structure
├── app.py # Streamlit app
├── src/ # helper modules, preprocessing, etc.
├── movie_list.pkl # small: movie id & title (tracked in repo)
├── similarity.pkl # large: precomputed similarity matrix (NOT in repo)
├── requirements.txt
└── README.md

yaml
Copy
Edit

> ⚠️ `similarity.pkl` can be large (>100MB) and should **not** be committed to GitHub. Use external hosting (Google Drive / Hugging Face / S3) and download at runtime — example included below.

---

## 💻 Run locally (development)
1. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Start the Streamlit app:

bash
Copy
Edit
streamlit run app.py
☁️ Deploy to Streamlit Cloud
Push your repo (without similarity.pkl) to GitHub.

In Streamlit Cloud, create a new app and connect to this GitHub repo/branch.

Ensure requirements.txt is present.

Host similarity.pkl externally (see below) so the app downloads it on first run.

🔗 Recommended way to host large similarity.pkl
Option A — Google Drive (simple)

Upload similarity.pkl to Google Drive and make it shareable.

Use gdown to download in the app.

Add gdown to your requirements.txt and use this snippet in app.py:

python
Copy
Edit
import os
import gdown
import pickle
import streamlit as st

# Replace with your Google Drive file ID
FILE_ID = "YOUR_GOOGLE_DRIVE_FILE_ID"
DRIVE_URL = f"https://drive.google.com/uc?id={FILE_ID}"
LOCAL_PATH = "similarity.pkl"

@st.cache_resource
def get_similarity():
    if not os.path.exists(LOCAL_PATH):
        gdown.download(DRIVE_URL, LOCAL_PATH, quiet=False)
    with open(LOCAL_PATH, "rb") as f:
        return pickle.load(f)

similarity = get_similarity()
Option B — Hugging Face / S3
Upload the file to a stable host and download it with requests the same way.

✅ Best practices
Add this to .gitignore:

bash
Copy
Edit
# Ignore large precomputed matrices
similarity.pkl
Keep movie_list.pkl (small mapping of movie_id → title) in the repo so the UI has titles.

Cache heavy loads in Streamlit with @st.cache_resource (or @st.cache_data where appropriate).

🛠 Troubleshooting
Push rejected due to large file: GitHub rejects files >100MB. If you accidentally committed a large file, remove it from history (use git filter-repo or BFG) or delete the repo and re-create without the large file.

Line-ending warnings on Windows: Run git config core.autocrlf true to avoid LF/CRLF warnings.

🤝 Contributing
Fork the repo

Create a branch feature/your-feature

Open a PR — explain your change and how to test it
