# app.py
import streamlit as st
from utils.extract_text import extract_resume_text
from utils.match_resume import get_similarity
from sklearn.feature_extraction.text import CountVectorizer

st.set_page_config(page_title="AI Resume Screener", layout="wide")

# ------------------------------
# 🔎 Keyword Extraction Helper
# ------------------------------
def extract_keywords(resume, job_desc, top_n=5):
    vectorizer = CountVectorizer(stop_words='english').fit([job_desc])
    jd_words = set(vectorizer.get_feature_names_out())
    resume_words = set(resume.lower().split())
    matched = list(jd_words & resume_words)
    return matched[:top_n]

# Inject custom CSS for background and styling
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://www.recruiterslineup.com/wp-content/uploads/2022/04/ai-resume-screening.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    .block-container {
        max-width: 900px;
        margin: auto;
        padding: 5vw 3vw;
        text-align: center;
    }

    h1, h2, h3, h4, .stSubheader {
        color: #FFFFFF !important;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        font-size: clamp(1.5rem, 2vw + 1rem, 2.5rem);
        text-shadow: 1px 1px 4px #000;
    }

    textarea {
        background-color: rgba(255,255,255,0.9) !important;
        color: #000 !important;
        border-radius: 10px;
        padding: 14px 18px;
        width: 100%;
        font-size: 1rem;
    }

    .stFileUploader {
        background-color: #f0f0f0 !important;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }

    .stFileUploader, .stButton {
        text-align: center;
    }

    .stButton > button {
        background-color: #007BFF !important;
        color: #ffffff !important;
        font-size: 16px;
        font-weight: bold;
        padding: 12px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        border: none;
        transition: transform 0.2s ease;
        width: 100%;
        max-width: 300px;
        margin: 20px auto;
        display: block;
    }

    .stButton > button:hover {
        transform: scale(1.05);
    }

    .result-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        border-left: 6px solid #28a745;
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }

    .match-score {
        font-weight: bold;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div style='padding: 30px 10px;'>
        <h1 style='color:white;'>🤖 AI-Powered Resume Screening System</h1>
        <h3 style='color:white;'>Match Resumes with Job Descriptions Using NLP & AI</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h4 style='color:white;'>Enter Job Description Below</h4>", unsafe_allow_html=True)

job_description = st.text_area("", height=200, placeholder="Paste the job description here...", max_chars=5000)

uploaded_files = st.file_uploader("📎 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("🔍 Analyze Resumes"):
    if job_description and uploaded_files:
        results = []
        with st.spinner("⏳ Processing resumes..."):
            for uploaded_file in uploaded_files:
                resume_text = extract_resume_text(uploaded_file)
                score = get_similarity(resume_text, job_description)
                keywords = extract_keywords(resume_text, job_description)
                results.append((uploaded_file.name, score, keywords))

        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

        st.success("✅ Resumes ranked by similarity!")
        st.subheader("📊 Results:")
        for name, score, keywords in sorted_results:
            st.markdown(f"""
                <div class='result-box'>
                    <strong>{name}</strong><br>
                    <span class='match-score'>Match Score: {score:.2f}</span><br>
                    <span style='font-size: 14px; color: #333;'>🔑 Matched Keywords: <i>{', '.join(keywords)}</i></span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please paste a job description and upload at least one resume.")
