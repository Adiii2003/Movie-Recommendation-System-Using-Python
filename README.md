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

## 🚀 Run locally (development)

1. Create and activate a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
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
Push your repo (do not include similarity.pkl) to GitHub.

In Streamlit Cloud, create a new app and connect it to this GitHub repo & branch.

Make sure requirements.txt is present.

Host similarity.pkl externally (Google Drive / Hugging Face / S3) and let the app download it at runtime (example below).

🔗 Recommended: host large similarity.pkl externally
similarity.pkl can be large (>100 MB). Do not commit it to GitHub.

Option A — Google Drive (simple)
Upload similarity.pkl to Google Drive and make the file shareable.

Add gdown to requirements.txt:

nginx
Copy
Edit
gdown
Use this snippet in app.py to download and load the file (only once per session):

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
Option B — Hugging Face / S3 / other host
Upload the file to a stable host and download it at runtime with requests or similar, then load with pickle.

✅ Best practices
Add to .gitignore:

bash
Copy
Edit
# Ignore large precomputed matrices
similarity.pkl
Keep movie_list.pkl (small mapping of movie_id → title) in the repo so the UI has titles.

Cache heavy loads in Streamlit using @st.cache_resource or @st.cache_data depending on the data type.

Do not commit files larger than 100 MB to GitHub. Use Git LFS or external hosting if necessary.

🛠 Troubleshooting
Push rejected: large file (>100MB)
GitHub rejects files over 100 MB. If you accidentally committed a large file, remove it from history with git filter-repo or BFG, or delete and recreate the repo (clean commit without the large file).

Line-ending warnings on Windows
Run:

bash
Copy
Edit
git config core.autocrlf true
🤝 Contributing


Open a Pull Request describing your change and how to test itange and how to test it
