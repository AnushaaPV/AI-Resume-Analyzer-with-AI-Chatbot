import streamlit as st

st.set_page_config(page_title="Resume Job Match Scorer", page_icon="📄", layout="wide")

# Hide Streamlit's default page list in the sidebar (we use our own buttons)
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

pages = [
    st.Page("home_page.py", title="Home", icon="🏠", default=True),
    st.Page("app_styled.py", title="Resume Matcher", icon="📄"),
]

pg = st.navigation(pages)
pg.run()
