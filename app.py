from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from docx import Document
import fitz  # PyMuPDF
import spacy
import re
import io
import os

# ---------------
# Flask setup
# ---------------
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB upload limit

# Load models once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')
# If the spaCy model isn't present, give a helpful error at startup
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise OSError("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")

# ----------------------
# Extract Text from Any File
# ----------------------
def extract_text(file_bytes, filename):
    filename = filename.lower()
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return " ".join(page.get_text() for page in doc)
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        return " ".join([para.text for para in doc.paragraphs])
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        return ""

# ----------------------
# Clean and Normalize
# ----------------------
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip().lower()

# ----------------------
# Improved Keyword Matching with TF-IDF
# ----------------------
def keyword_match_spacy(resume_text, jd_text, top_k=20):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=top_k)
    tfidf_matrix = vectorizer.fit_transform([jd_text])
    jd_keywords = vectorizer.get_feature_names_out()

    matched = [kw for kw in jd_keywords if kw.lower() in resume_text]
    missing = list(set(jd_keywords) - set(matched))

    match_percent = (len(matched) / len(jd_keywords) * 100) if len(jd_keywords) else 0.0
    return round(match_percent, 2), missing

# ----------------------
# Confidence Label
# ----------------------
def fit_label(score):
    if score >= 80:
        return "Strong Fit"
    elif score >= 60:
        return "Moderate Fit"
    else:
        return "Low Fit"

# ----------------------
# Recommendation (keywords only)
# ----------------------
def generate_recommendation(missing_keywords):
    if missing_keywords:
        return f"Consider adding relevant keywords like: {', '.join(sorted(missing_keywords))}."
    return "Great alignment with the job description!"

# ----------------------
# Web UI
# ----------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# ----------------------
# API Endpoint
# ----------------------
@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    if 'file' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "file and job_description are required"}), 400

    file = request.files['file']
    job_description = request.form['job_description']
    filename = file.filename or ""
    if not filename.lower().endswith((".pdf", ".docx", ".txt")):
        return jsonify({"error": "Unsupported file type. Use PDF, DOCX, or TXT."}), 400

    resume_bytes = file.read()
    resume_text = extract_text(resume_bytes, filename)
    if not resume_text.strip():
        return jsonify({"error": "Could not read text from the uploaded file."}), 400

    resume_text = clean_text(resume_text)
    jd_text = clean_text(job_description)

    # Semantic Similarity
    emb_resume = model.encode(resume_text, convert_to_tensor=True, normalize_embeddings=True)
    emb_jd = model.encode(jd_text, convert_to_tensor=True, normalize_embeddings=True)
    match_score = float(util.cos_sim(emb_resume, emb_jd)[0][0]) * 100

    # Keyword Matching
    keyword_match_percent, missing_keywords = keyword_match_spacy(resume_text, jd_text)

    # Response
    result = {
        "match_score": round(match_score, 2),
        "keyword_match": keyword_match_percent,
        "missing_keywords": sorted(missing_keywords),
        "fit_level": fit_label(match_score),
        "recommendation": generate_recommendation(missing_keywords)
    }
    # If request is from the web UI, return HTML; if it's an API client, return JSON.
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        return jsonify(result)
    else:
        # Render the result inline
        return render_template("index.html", result=result)

if __name__ == '__main__':
    # For local dev only
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)