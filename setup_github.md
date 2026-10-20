# EcoGenieBot Deployment Notes

The repository already exists at [github.com/LuckyNawale/EcoGenieBot](https://github.com/LuckyNawale/EcoGenieBot). Do not create a duplicate repository for deployment.

## Deploy on Streamlit Community Cloud

1. Push the current project files to the branch you intend to deploy. The app requires `app.py`, `chatbot.py`, `intents.json`, and `requirements.txt` at the repository root.
2. Open the [Streamlit Community Cloud deploy page](https://share.streamlit.io/deploy?repository=LuckyNawale%2FEcoGenieBot&branch=main&mainModule=app.py) and sign in/connect your GitHub account.
3. Choose repository `LuckyNawale/EcoGenieBot`, branch `main`, and main file `app.py`.
4. Deploy, wait for startup, then test known and unknown messages in the hosted app.
5. Add the URL assigned by Streamlit to the Demo section in `README.md` only after confirming the app works.

The current version reads `intents.json` directly and fits its vectorizer at startup. It does not require model pickle files, a local data path, NLTK downloads, or environment secrets.

## Local Verification

From the repository root on Windows:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

For the complete project architecture, V1/V2 comparison, rebuild notes, interview guide, and troubleshooting, see [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md).