import os
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("averaged_perceptron_tagger_eng", quiet=True)

# (page setup is done in main.py)

DEFAULT_MODEL = "gemini-3.8-flash"

# ---------------- Custom CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Poppins', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #fdf2ff 0%, #eef3ff 50%, #e8fbff 100%);
    color: #2d2a4a;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1100px; }

/* Force readable text colors (works in light or dark Streamlit theme) */
.stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp [data-testid="stWidgetLabel"] p { color: #2d2a4a; }

/* Hero */
.hero {
    background: linear-gradient(120deg, #6a11cb 0%, #8e44ad 40%, #ff6a95 100%);
    border-radius: 24px;
    padding: 2.4rem 2.6rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 18px 40px rgba(106, 17, 203, 0.25);
    position: relative;
    overflow: hidden;
}
.hero::before, .hero::after {
    content: "";
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.12);
}
.hero::before { width: 220px; height: 220px; right: -50px; top: -70px; }
.hero::after  { width: 130px; height: 130px; right: 120px; bottom: -60px; }
.hero h1 { color: #ffffff !important; font-size: 2.3rem; font-weight: 700; margin: 0 0 .4rem 0; }
.hero p  { color: rgba(255,255,255,0.92) !important; font-size: 1.02rem; margin: 0; max-width: 640px; }
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: #fff;
    padding: .25rem .8rem;
    border-radius: 999px;
    font-size: .78rem;
    font-weight: 500;
    margin-bottom: .8rem;
    backdrop-filter: blur(4px);
}

/* Section titles */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    margin: 0 0 .6rem 0;
    color: #4a2c8a;
}

/* Cards (applied to input widgets) */
[data-testid="stFileUploader"] section {
    background: #ffffff;
    border: 2px dashed #b794f4;
    border-radius: 18px;
    padding: 1.2rem;
    transition: all .25s ease;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #6a11cb;
    box-shadow: 0 8px 22px rgba(106, 17, 203, 0.15);
}
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploader"] section span { color: #5b5780 !important; }
[data-testid="stFileUploader"] button { border-radius: 10px; }

.stTextArea textarea {
    background: #ffffff !important;
    color: #2d2a4a !important;
    border: 2px solid #e4d9f7 !important;
    border-radius: 18px !important;
    padding: 1rem !important;
    font-family: 'Poppins', sans-serif;
}
.stTextArea textarea:focus {
    border-color: #8e44ad !important;
    box-shadow: 0 0 0 3px rgba(142, 68, 173, 0.18) !important;
}

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(120deg, #6a11cb, #ff6a95);
    color: #fff;
    border: none;
    border-radius: 14px;
    padding: .8rem 1.2rem;
    font-size: 1.05rem;
    font-weight: 600;
    box-shadow: 0 10px 24px rgba(106, 17, 203, 0.28);
    transition: transform .2s ease, box-shadow .2s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(255, 106, 149, 0.35);
    color: #fff;
}
.stButton > button:active { transform: translateY(0); }
.stButton > button p, .stButton > button span { color: #ffffff !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2b1055 0%, #4a2c8a 100%);
}
[data-testid="stSidebar"] * { color: #f3ecff !important; }
.side-card {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    font-size: .9rem;
    line-height: 1.7;
}
.side-title { font-weight: 600; font-size: 1.05rem; margin-bottom: .4rem; }

/* Result score card */
.score-card {
    background: #ffffff;
    border-radius: 24px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 14px 34px rgba(74, 44, 138, 0.12);
}
.ring {
    width: 190px;
    height: 190px;
    border-radius: 50%;
    margin: 0 auto 1rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
}
.ring-inner {
    width: 146px;
    height: 146px;
    border-radius: 50%;
    background: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.06);
}
.ring-score { font-size: 2.2rem; font-weight: 700; color: #2d2a4a; line-height: 1; }
.ring-label { font-size: .8rem; color: #7a76a0; margin-top: .3rem; }
.verdict {
    display: inline-block;
    padding: .4rem 1.1rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: .95rem;
}

/* Keyword chips */
.chip-box {
    background: #ffffff;
    border-radius: 24px;
    padding: 1.6rem 1.6rem 1.2rem 1.6rem;
    box-shadow: 0 14px 34px rgba(74, 44, 138, 0.12);
    height: 100%;
}
.chip {
    display: inline-block;
    padding: .35rem .85rem;
    margin: 0 .4rem .5rem 0;
    border-radius: 999px;
    font-size: .85rem;
    font-weight: 500;
}
.chip-ok   { background: #e3f9ef; color: #137a52; border: 1px solid #b6ecd3; }
.chip-miss { background: #ffe9ee; color: #b3264a; border: 1px solid #ffc7d3; }
.chip-title { font-weight: 600; color: #4a2c8a; margin: .4rem 0 .6rem 0; font-size: .95rem; }

/* AI chat */
.chat-head {
    background: linear-gradient(120deg, #2b1055, #6a11cb);
    border-radius: 20px;
    padding: 1.2rem 1.5rem;
    margin: 2rem 0 1rem 0;
    box-shadow: 0 14px 34px rgba(74, 44, 138, 0.2);
}
.chat-head h3 { color: #ffffff !important; margin: 0 0 .25rem 0; font-size: 1.2rem; font-weight: 600; }
.chat-head p  { color: rgba(255,255,255,0.85) !important; margin: 0; font-size: .92rem; }
[data-testid="stChatMessage"] {
    background: #ffffff;
    border-radius: 18px;
    padding: 1rem 1.1rem;
    margin-bottom: .8rem;
    box-shadow: 0 8px 22px rgba(74, 44, 138, 0.08);
}
[data-testid="stChatInput"] {
    background: #ffffff;
    border: 2px solid #e4d9f7;
    border-radius: 18px;
}
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #2d2a4a !important;
}
[data-testid="stBottom"] > div { background: transparent; }

/* Footer */
.footer { text-align: center; color: #7a76a0; font-size: .85rem; margin-top: 2.5rem; }

/* Hide default Streamlit chrome */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown("""
    <div class="side-card">
        <div class="side-title">✨ About</div>
        This tool helps you:<br>
        • Measure how well your resume matches a job description<br>
        • Spot the important job keywords<br>
        • Improve your resume using missing terms<br>
        • Chat with an AI resume coach
    </div>
    <div class="side-card">
        <div class="side-title">🚀 How it works</div>
        1. Upload your resume (PDF)<br>
        2. Paste the job description<br>
        3. Click <b>Analyze Match</b><br>
        4. Review your score and suggestions<br>
        5. Ask the AI coach for help
    </div>
    """, unsafe_allow_html=True)

# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
    <span class="badge">TF-IDF + Cosine Similarity + Gemini AI</span>
    <h1>📄 Resume Job Match Scorer</h1>
    <p>Upload your resume, paste a job description, and see how closely they match.
    Find the keywords you are missing, then ask the AI coach how to fix them.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- Helper functions ----------------
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text = text + (page.extract_text() or "")
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_stopwords(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    return " ".join([word for word in words if word not in stop_words])


def calculate_similarity(resume_text, job_description):
    resume_processed = remove_stopwords(clean_text(resume_text))
    job_processed = remove_stopwords(clean_text(job_description))
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_processed, job_processed])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100
    return round(score, 2), resume_processed, job_processed


def extract_keywords(text, num_keywords=10):
    words = word_tokenize(text)
    words = [w for w in words if len(w) > 2]
    tagged_words = pos_tag(words)
    nouns = [w for w, pos in tagged_words if pos.startswith("NN") or pos.startswith("JJ")]
    word_freq = Counter(nouns)
    return word_freq.most_common(num_keywords)


def score_ring(score):
    if score < 40:
        color, bg, text, verdict = "#ff6b6b", "#ffe9e9", "#b3262a", "Low match"
    elif score < 70:
        color, bg, text, verdict = "#ffb347", "#fff2dd", "#a15c00", "Good match"
    else:
        color, bg, text, verdict = "#2ecc9a", "#e3f9ef", "#137a52", "Excellent match"
    degrees = score * 3.6
    return f"""
    <div class="score-card">
        <div class="ring" style="background: conic-gradient({color} {degrees}deg, #eee8f8 0deg);">
            <div class="ring-inner">
                <div class="ring-score">{score:.1f}%</div>
                <div class="ring-label">match score</div>
            </div>
        </div>
        <span class="verdict" style="background:{bg}; color:{text};">{verdict}</span>
    </div>
    """


def chips(words, css_class):
    if not words:
        return "<span style='color:#7a76a0; font-size:.9rem;'>None</span>"
    return "".join(f'<span class="chip {css_class}">{w}</span>' for w in words)


# ---------------- Gemini chatbot helpers ----------------
def get_secret(name):
    """Read a value from .streamlit/secrets.toml, then from environment variables."""
    try:
        return st.secrets[name]
    except Exception:
        return os.environ.get(name)


def build_system_prompt(a):
    return f"""You are a friendly resume coach helping a job seeker.

Rules:
- Use plain, simple English. Keep answers short and practical.
- Base your advice only on the resume and job description below.
- Never invent experience, skills, tools, numbers or achievements the person does not have.
- If a keyword is missing, tell the person to add it only if it is true for them.
- If asked to rewrite something, use only facts that are in the resume.

MATCH SCORE: {a['score']}%
KEYWORDS FOUND IN RESUME: {', '.join(a['matched']) or 'none'}
KEYWORDS MISSING FROM RESUME: {', '.join(a['missing']) or 'none'}

RESUME:
{a['resume_text'][:6000]}

JOB DESCRIPTION:
{a['job_description'][:4000]}
"""


def ask_gemini(question, history, analysis):
    api_key = get_secret("GEMINI_API_KEY")
    model = get_secret("GEMINI_MODEL") or DEFAULT_MODEL

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return "The Gemini library is not installed. Run `pip install -U google-genai` and restart the app."

    try:
        client = genai.Client(api_key=api_key)
        contents = []
        for m in history:
            role = "user" if m["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=m["content"])]))
        contents.append(types.Content(role="user", parts=[types.Part(text=question)]))

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=build_system_prompt(analysis)),
        )
        return response.text or "I could not generate an answer. Please try asking in a different way."
    except Exception as e:
        return (
            "Something went wrong while contacting Gemini.\n\n"
            f"`{str(e)[:300]}`\n\n"
            "Check that your API key is correct. If it says the model was not found, "
            "set `GEMINI_MODEL` in your secrets file to a current model name from Google AI Studio."
        )


def render_chat(analysis):
    st.markdown("""
    <div class="chat-head">
        <h3>🤖 AI Resume Coach</h3>
        <p>Ask how to add missing keywords, improve your summary, or tailor your resume for this job.</p>
    </div>
    """, unsafe_allow_html=True)

    if not get_secret("GEMINI_API_KEY"):
        st.info(
            "To turn on the AI coach, add your free Gemini API key.\n\n"
            "1. Get a key at aistudio.google.com/apikey\n"
            "2. Create the file `.streamlit/secrets.toml` in your project folder\n"
            "3. Add this line: `GEMINI_API_KEY = \"your-key-here\"`\n"
            "4. Restart the app"
        )
        return

    st.caption("Your resume text is sent to Google's Gemini API to generate answers. "
               "Try: “How can I add the missing keywords?” or “Rewrite my summary for this job.”")

    for m in st.session_state["messages"]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask the AI coach about your resume...")
    if prompt:
        history = list(st.session_state["messages"])
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = ask_gemini(prompt, history, analysis)
            st.markdown(reply)
        st.session_state["messages"].append({"role": "assistant", "content": reply})


# ---------------- Main app ----------------
def main():
    st.session_state.setdefault("analysis", None)
    st.session_state.setdefault("messages", [])

    st.page_link("home_page.py", label="← Back to home", icon="🏠")
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown('<div class="section-title">📎 Your resume</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], label_visibility="collapsed")

    with right:
        st.markdown('<div class="section-title">📝 Job description</div>', unsafe_allow_html=True)
        job_description = st.text_area(
            "Paste the job description",
            height=200,
            placeholder="Paste the full job description here...",
            label_visibility="collapsed",
        )

    st.write("")
    clicked = st.button("✨ Analyze Match")

    if clicked:
        if not uploaded_file:
            st.warning("Please upload your resume")
            return
        if not job_description:
            st.warning("Please paste the job description")
            return

        with st.spinner("Analyzing your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text:
                st.error("Could not extract text from the PDF. Please try another PDF.")
                return

            similarity_score, resume_processed, job_processed = calculate_similarity(resume_text, job_description)

            # Keyword gap
            job_keywords = [w for w, _ in extract_keywords(job_processed, 15)]
            resume_words = set(resume_processed.split())
            matched = [w for w in job_keywords if w in resume_words]
            missing = [w for w in job_keywords if w not in resume_words]

        # Save results so they stay on screen while chatting, and start a fresh chat
        st.session_state["analysis"] = {
            "score": similarity_score,
            "matched": matched,
            "missing": missing,
            "resume_text": resume_text,
            "job_description": job_description,
        }
        st.session_state["messages"] = []

    analysis = st.session_state["analysis"]

    if analysis:
        st.write("")
        st.markdown('<div class="section-title">📊 Results</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1.4], gap="large")

        with col1:
            st.markdown(score_ring(analysis["score"]), unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="chip-box">
                <div class="chip-title">✅ Keywords found in your resume</div>
                {chips(analysis["matched"], "chip-ok")}
                <div class="chip-title" style="margin-top:1rem;">💡 Keywords to consider adding</div>
                {chips(analysis["missing"], "chip-miss")}
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        score = analysis["score"]
        if score < 40:
            st.warning("Low match. Consider tailoring your resume more closely to this job.")
        elif score < 70:
            st.info("Good match. Your resume aligns fairly well.")
        else:
            st.success("Excellent match! Your resume strongly aligns.")

        render_chat(analysis)

    st.markdown('<div class="footer">Built with Streamlit, scikit-learn, NLTK and Gemini</div>', unsafe_allow_html=True)


main()