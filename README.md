# AI Resume Analyzer with AI Chatbot

A Streamlit web app that scores how well a resume matches a job description, shows which job keywords are missing, and lets you chat with an AI resume coach.

 **Live demo:** https://ai-resume-analyzer-with-ai-coach-7mcdcy6gdlkd2pquhobxgq.streamlit.app/

## Features

- Upload a resume (PDF) and paste a job description
- Match score using TF-IDF and cosine similarity
- Keywords found in your resume and keywords you may want to add
- AI Resume Coach (Google Gemini) that answers questions about your resume and the job
- Home page and analyzer page with custom styling

## Tech used

Python, Streamlit, scikit-learn, NLTK, PyPDF2, Google Gemini API

## How to run

1. Install the libraries:

   ```
   pip install -r requirements.txt
   ```

2. Get a free Gemini API key at https://aistudio.google.com/apikey

3. Create a file `.streamlit/secrets.toml` and add your key:

   ```
   GEMINI_API_KEY = "your-key-here"
   ```

   Optional: set a different model with `GEMINI_MODEL = "model-name"`.

4. Start the app:

   ```
   streamlit run main.py
   ```

## Project files

- `main.py` - starts the app and sets up the pages
- `home_page.py` - home page
- `app_styled.py` - resume analyzer page and AI coach

## Notes

- The match score is based on word overlap, so it is a rough guide and not a judgment of your skills.
- When you use the AI coach, your resume text is sent to Google's Gemini API.
- Never upload your `secrets.toml` file or API key to GitHub.
