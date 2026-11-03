import streamlit as st

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #fdf2ff 0%, #eef3ff 50%, #e8fbff 100%);
    color: #2d2a4a;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1100px; }

/* No sidebar on the home page */
[data-testid="stSidebar"], [data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] { display: none; }

#MainMenu, footer { visibility: hidden; }

/* Hero */
.home-hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    background: linear-gradient(120deg, #6a11cb 0%, #8e44ad 45%, #ff6a95 100%);
    border-radius: 32px;
    padding: 4.2rem 2rem 3.4rem 2rem;
    box-shadow: 0 24px 60px rgba(106, 17, 203, 0.28);
}
.blob {
    position: absolute;
    border-radius: 50%;
    background: rgba(255,255,255,0.13);
    animation: float 7s ease-in-out infinite;
}
.blob.b1 { width: 260px; height: 260px; left: -70px; top: -90px; }
.blob.b2 { width: 160px; height: 160px; right: 6%; top: 18%; animation-delay: 1.5s; }
.blob.b3 { width: 200px; height: 200px; right: -60px; bottom: -80px; animation-delay: 3s; }
.blob.b4 { width: 90px; height: 90px; left: 12%; bottom: 14%; animation-delay: 2s; }
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-18px); }
}
.home-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: #fff;
    padding: .35rem 1rem;
    border-radius: 999px;
    font-size: .85rem;
    font-weight: 500;
    margin-bottom: 1.2rem;
    position: relative;
}
.home-hero h1 {
    position: relative;
    color: #ffffff !important;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 1rem 0;
}
.home-hero p {
    position: relative;
    color: rgba(255,255,255,0.93) !important;
    font-size: 1.1rem;
    max-width: 620px;
    margin: 0 auto;
}

/* CTA button */
.stButton > button {
    width: 100%;
    background: linear-gradient(120deg, #ff6a95, #6a11cb);
    color: #fff;
    border: none;
    border-radius: 16px;
    padding: 1rem 1.2rem;
    font-size: 1.1rem;
    font-weight: 600;
    box-shadow: 0 14px 30px rgba(106, 17, 203, 0.32);
    transition: transform .2s ease, box-shadow .2s ease;
    margin-top: -1.4rem;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 18px 38px rgba(255, 106, 149, 0.4);
    color: #fff;
}
.stButton > button:active { transform: translateY(0); }

/* Section heading */
.sec-title {
    text-align: center;
    font-size: 1.7rem;
    font-weight: 700;
    color: #4a2c8a;
    margin: 3.2rem 0 .4rem 0;
}
.sec-sub { text-align: center; color: #6b678f; margin-bottom: 1.8rem; }

/* Feature cards */
.cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.4rem; }
.card {
    background: #ffffff;
    border-radius: 22px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    box-shadow: 0 12px 30px rgba(74, 44, 138, 0.10);
    transition: transform .25s ease, box-shadow .25s ease;
}
.card:hover { transform: translateY(-6px); box-shadow: 0 18px 38px rgba(74, 44, 138, 0.18); }
.card .icon {
    width: 64px; height: 64px;
    border-radius: 18px;
    margin: 0 auto 1rem auto;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.9rem;
    background: linear-gradient(135deg, #f3e8ff, #ffe4ee);
}
.card h3 { color: #4a2c8a !important; font-size: 1.1rem; font-weight: 600; margin: 0 0 .5rem 0; }
.card p { color: #5b5780 !important; font-size: .93rem; margin: 0; line-height: 1.6; }

/* Steps */
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; }
.step { text-align: center; padding: 1rem .6rem; }
.step .num {
    width: 46px; height: 46px; border-radius: 50%;
    margin: 0 auto .8rem auto;
    display: flex; align-items: center; justify-content: center;
    color: #fff; font-weight: 700;
    background: linear-gradient(120deg, #6a11cb, #ff6a95);
    box-shadow: 0 8px 18px rgba(106, 17, 203, 0.25);
}
.step p { color: #2d2a4a !important; font-weight: 500; font-size: .95rem; margin: 0; }

.home-footer { text-align: center; color: #7a76a0; font-size: .85rem; margin: 3rem 0 1rem 0; }

@media (max-width: 800px) {
    .cards, .steps { grid-template-columns: 1fr; }
    .home-hero h1 { font-size: 2.1rem; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- Hero ----------------
st.markdown("""
<div class="home-hero">
    <div class="blob b1"></div>
    <div class="blob b2"></div>
    <div class="blob b3"></div>
    <div class="blob b4"></div>
    <span class="home-badge">📄 AI Resume Analyzer</span>
    <h1>Does your resume match<br>the job you want?</h1>
    <p>Upload your resume, paste a job description, and get an instant match score
    with the keywords you are missing.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- Call to action ----------------
_, mid, _ = st.columns([1, 1.3, 1])
with mid:
    if st.button("🚀 Check your resume matching score"):
        st.switch_page("app_styled.py")

# ---------------- Features ----------------
st.markdown("""
<div class="sec-title">What you get</div>
<div class="sec-sub">Simple, quick and focused on what recruiters' systems look for.</div>
<div class="cards">
    <div class="card">
        <div class="icon">🎯</div>
        <h3>Match score</h3>
        <p>See how closely your resume matches a job description as a percentage.</p>
    </div>
    <div class="card">
        <div class="icon">🔑</div>
        <h3>Keyword gap</h3>
        <p>Find the important job keywords that are missing from your resume.</p>
    </div>
    <div class="card">
        <div class="icon">✍️</div>
        <h3>Tailor with ease</h3>
        <p>Use the missing keywords to adjust your resume for each application.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- Steps ----------------
st.markdown("""
<div class="sec-title">How it works</div>
<div class="sec-sub">Four quick steps.</div>
<div class="steps">
    <div class="step"><div class="num">1</div><p>Click the button above</p></div>
    <div class="step"><div class="num">2</div><p>Upload your resume (PDF)</p></div>
    <div class="step"><div class="num">3</div><p>Paste the job description</p></div>
    <div class="step"><div class="num">4</div><p>Review your score</p></div>
</div>
<div class="home-footer">Built with Streamlit, scikit-learn and NLTK</div>
""", unsafe_allow_html=True)