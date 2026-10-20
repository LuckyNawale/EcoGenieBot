# EcoGenieBot

An intent-based chatbot prototype for sustainability and green technology questions. It matches a user's message to examples in a JSON intent dataset and returns a response associated with the closest match.

Originally developed as an AICTE internship project in 2024. The current runnable version is a cleaned-up TF-IDF similarity matcher; see the project handbook for how it differs from the early Logistic Regression experiments.

## Demo

Live demo: not deployed yet. The app can be deployed for free with [Streamlit Community Cloud](https://share.streamlit.io/deploy?repository=LuckyNawale%2FEcoGenieBot&branch=main&mainModule=app.py).

## Run Locally

```powershell
git clone https://github.com/LuckyNawale/EcoGenieBot.git
cd EcoGenieBot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
streamlit run app.py
```

## How It Works

1. `intents.json` stores intent tags, example user messages, and candidate responses.
2. `chatbot.py` normalizes text and builds TF-IDF vectors from the example messages using one- and two-word n-grams.
3. The user's message is vectorized and compared with the examples using cosine similarity.
4. The closest example's intent is used if its similarity reaches the confidence threshold; otherwise the bot asks the user to rephrase.
5. `app.py` presents the exchange in a Streamlit chat interface.

This is a retrieval-style intent matcher, not a generative AI model. Its replies are selected from the dataset.

## Repository Map

- `app.py`: Streamlit user interface.
- `chatbot.py`: intent matching and response selection.
- `intents.json`: chatbot examples and responses.
- `tests/`: focused tests for known, unknown, and legacy-shaped intent data.
- `legacy_streamlit_app.py`, `01app.py`, `PROJECT/`, `notebooks/`: internship-era experiments; they may refer to artifacts or paths that are not part of the runnable app.
- `INTERVIEW_GUIDE.md`: architecture refresher, demo script, limitations, and interview practice questions.

## Scope and Limitations

- Replies are limited to the examples and responses in `intents.json`.
- Similarity matching can confuse intents with overlapping wording; the threshold is a simple heuristic, not a calibrated probability.
- The project has no published accuracy score or formal held-out evaluation, so do not claim one.
- It does not currently provide live weather, current time, or free-form factual answers.
- Verify environmental advice with authoritative sources.

## Project Handbook

Read [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) for the rebuild instructions, V1-to-V2 comparison, architecture walkthrough, demo script, troubleshooting, deployment steps, and interview practice questions.
