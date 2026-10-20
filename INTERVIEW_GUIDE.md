# EcoGenieBot Project Handbook and Interview Guide

This is the project memory document: use it to understand the internship-era prototype, rebuild the current app on a fresh machine, demo it, and answer technical follow-ups. You said you built the project in 2024; confirm the exact dates and your personal contribution from your own records before putting them on a resume.

## Start Here After a Long Break

The supported version is made from these files:

- `app.py`: Streamlit chat interface and per-session message history.
- `chatbot.py`: intent data loading, text normalization, TF-IDF matching, fallback, and response selection.
- `intents.json`: intent tags, example messages, and canned responses.
- `requirements.txt`: Python packages needed by the app.
- `tests/test_chatbot.py`: behavior checks for known, blank, unsupported, and legacy-shaped data.

The notebooks and scripts under `PROJECT/`, `notebooks/`, `01app.py`, and `legacy_streamlit_app.py` are historical experiments, not the v2 launch path. In particular, some expect missing pickle files, use older data layouts, or have machine-specific assumptions. Start with the five supported files above.

## Run It From a Fresh Windows Machine

Install Python 3.10 or newer, then open PowerShell in the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. To rebuild the checkout itself rather than just its environment:

```powershell
git clone https://github.com/LuckyNawale/EcoGenieBot.git
Set-Location EcoGenieBot
```

Then run the setup commands above. A virtual environment keeps this project's packages isolated from other Python projects. `.venv/` is ignored by Git and should not be committed.

## What the Project Does

EcoGenieBot answers supported sustainability and green-technology questions by selecting a canned response associated with a matching intent. It does not generate answers, call an LLM, browse the web, or provide live environmental data.

The current request path is:

```text
intents.json -> normalize patterns -> fit TF-IDF vectors at startup
user message -> normalize -> vectorize -> cosine similarity to every pattern
                         -> best pattern's intent -> threshold check
                         -> choose a stored response, or return a clarification prompt
```

`app.py` renders the conversation. `chatbot.py` owns the response decision, so the matching logic can be tested without launching a browser. Streamlit session state preserves the conversation while that browser session is active; this is not permanent database storage.

## Version 1 Versus Version 2

| Area | Internship-era V1 experiments | Current V2 supported app |
| --- | --- | --- |
| Goal | Explore a chatbot trained from example utterances | Provide a small, repeatable sustainability chatbot demo |
| NLP approach | The historical `PROJECT/chatbot.py` uses TF-IDF plus Logistic Regression to predict an intent tag | `chatbot.py` compares the message directly to all example patterns with TF-IDF and cosine similarity |
| Response | Predicted tag selects a response from the intent data | Highest-scoring pattern supplies a tag; response is randomly selected from that tag |
| UI/history | Early Streamlit experiments; `PROJECT/app.py` also writes a local CSV chat log | Chat-style Streamlit UI with browser-session message history |
| Startup | Some experiments download NLTK data, assume local files, or refer to saved model artifacts | Reads tracked `intents.json`; fits the vectorizer in memory; no NLTK download or pickle required |
| Organization | Notebook and script experiments overlap and are not all runnable together | UI, matching logic, data, dependencies, and tests have clear separate roles |
| Reliability | No focused test suite is part of the old experiment flow | Four unit tests cover core response behavior and compatibility with a singular `response` field |

V1 and V2 are not the same model with a new interface. V1's Logistic Regression experiment classifies an input into a learned label. V2 is retrieval-style matching against examples and deliberately does not fit Logistic Regression. The repository contains several V1 experiments, so describe them as exploration unless you can verify which exact version you personally completed or demonstrated in 2024.

## Rebuild the Basic V1 Concept

The smallest conceptual version is a script or notebook, without a web UI:

1. Create a small intent dataset. Each intent has a `tag`, a list of `patterns`, and a list of `responses`.
2. Flatten all patterns into one training list and repeat the pattern's tag in a label list.
3. Fit `TfidfVectorizer` on the patterns, then fit `LogisticRegression` on the vectors and intent labels.
4. For a user message, call the same vectorizer's `transform`, predict the intent tag, find that intent in the JSON data, and select one of its responses.
5. Add a simple input/output loop. The old Streamlit experiments wrapped this flow in a text input and displayed the response.

The core classifier flow is:

```text
patterns -> TF-IDF fit_transform -> LogisticRegression.fit(pattern_vectors, tags)
message  -> TF-IDF transform     -> classifier.predict -> intent tag -> response
```

This baseline has no natural-language understanding beyond patterns and learned word weights. A classifier always picks a class, including for unrelated questions, unless a rejection rule is added. Historical scripts also show why the experiment needed cleanup: some import/download NLTK data unnecessarily, one expects `vectorizer.pkl` and `model.pkl` that are not tracked, and an old helper script is incomplete. Those files are useful as history, not as rebuild instructions.

## Rebuild the Current V2 From Its Parts

If starting from an empty directory, create this minimum structure:

```text
EcoGenieBot/
|-- app.py
|-- chatbot.py
|-- intents.json
|-- requirements.txt
|-- tests/
|   `-- test_chatbot.py
`-- .gitignore
```

Build in this order:

1. **Data:** make `intents.json` valid JSON with one top-level `intents` array. Each item needs a unique `tag`, one or more `patterns`, and one or more `responses`. The current loader also accepts the old singular key `response` for compatibility.
2. **Matcher:** in `chatbot.py`, load the data relative to `Path(__file__)`, normalize text, flatten patterns and tags, and map each tag to its responses. Fit one `TfidfVectorizer(ngram_range=(1, 2))` on the normalized patterns when the bot is initialized.
3. **Reply method:** normalize the incoming message, return a prompt if it is empty, transform it with the fitted vectorizer, calculate cosine similarities against all pattern vectors, and select the tag for the highest-scoring pattern. If the score is below the threshold (currently `0.3`), return a clarification prompt; otherwise choose a response for that tag.
4. **Interface:** in `app.py`, configure the page, load one bot with `st.cache_resource`, render messages from `st.session_state`, accept text using `st.chat_input`, call `respond`, and append both sides of the exchange to session state.
5. **Dependencies and checks:** list Streamlit and scikit-learn in `requirements.txt`; add tests that cover a known pattern, blank input, a genuinely out-of-vocabulary input, and the supported legacy response shape.
6. **Run:** use the PowerShell commands in “Run It From a Fresh Windows Machine.”

Example data shape:

```json
{
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["hello", "hi there", "good morning"],
            "responses": ["Hello! What would you like to know about sustainability?"]
        }
    ]
}
```

When adding an intent, add several realistic ways a person might ask the same thing. Keep tags unique, use the same response key consistently (`responses`), validate JSON syntax, and include a test utterance. More patterns improve coverage but do not guarantee semantic understanding.

## NLP Terms in Plain Language

- **Intent:** the category of the user's goal, such as greeting or asking about recycling.
- **Pattern:** a sample user message assigned to an intent.
- **TF-IDF:** turns text into weighted word features. A word that appears in many examples is less distinctive than one that appears in fewer examples.
- **Unigram and bigram:** the current vectorizer considers individual words and adjacent two-word phrases.
- **Cosine similarity:** compares the direction of two text vectors. It is a similarity score, not a probability or guarantee that an answer is correct.
- **Threshold:** the manually selected minimum score for answering. The current `0.3` is a heuristic, not a calibrated confidence level; tune it using held-out examples, not one anecdotal prompt.
- **Classifier vs retrieval:** V1 predicts an intent class; V2 retrieves the closest stored example and uses its intent.

The matcher lowercases text and replaces non-ASCII letters, digits, and spaces with spaces. That is adequate for the small English-language dataset but can lose accents and does not support multilingual text well.

## Interview Demo: Five Minutes

1. Start with `streamlit run app.py` and explain that the app is an intent-based prototype, not generative AI.
2. Type a greeting. Show the matching example/tag in `intents.json` and the response list.
3. Ask a sustainability question using a stored pattern. Trace it through preprocessing, vectorization, similarity scoring, and response selection.
4. Ask an unrelated phrase with no shared vocabulary to show the fallback. A phrase containing a supported topic may still match that topic even if extra unrelated words are added.
5. Show the tests, then explain that a production-quality evaluation would need a held-out set and metrics. Do not report an accuracy number because this repository has no formal evaluation result.

Run the demo yourself shortly before an interview. The selected reply can vary because a response is chosen randomly from the matched intent.

## Likely Interview Questions

### Why TF-IDF and cosine similarity in V2?

They make a small, local, easy-to-inspect baseline without a large model or external service. The tradeoff is lexical matching: paraphrases with little word overlap can fail, and similar topics can be confused.

### Did you train a model?

In the V1 experiment, TF-IDF features were used to fit a Logistic Regression intent classifier. In the current V2 app, the vectorizer learns its vocabulary and weights from the patterns, but there is no separate classifier: the app uses cosine similarity to retrieve the closest example. Be clear which version the question refers to.

### How does the fallback work?

The matcher finds the highest similarity and compares it to a manually configured threshold. Under the threshold, it asks the user to rephrase. This does not prove the model knows or does not know an answer; it is a basic rejection heuristic.

### How would you evaluate it?

Create a held-out set of unseen messages labeled with expected intents. Report accuracy and per-class precision, recall, and F1, inspect a confusion matrix, and separately test out-of-scope rejection. Tune the threshold on validation data and keep the final test set untouched. There are no evaluation metrics in this repository today.

### What are the limitations?

The data controls the bot's coverage; response text is canned; word-based similarity does not capture meaning reliably; intent overlap can cause false matches; and the app does not do live lookup or general factual answering. The similarity score is not calibrated confidence.

### What did you improve when revisiting it?

The current supported path has a clear UI/core/data split, loads checked-in JSON through a path relative to the code, builds the vectorizer locally, avoids startup downloads and absent pickle files, handles the legacy singular response key, and has focused tests. Only claim work you personally made or can verify from the repository history.

### How would you improve it next?

Start with representative evaluation data and error analysis, then expand and deduplicate patterns, tune the fallback threshold, and add input validation. Compare a supervised classifier or sentence embeddings only if measurements show the simple matcher is inadequate. Persist chat history only if there is a real product need and a privacy plan.

## Troubleshooting

- **`ModuleNotFoundError` for `streamlit` or `sklearn`:** activate `.venv`, then run `python -m pip install -r requirements.txt`.
- **App starts from the wrong directory:** run `streamlit run app.py` from the repository root; the data path is resolved relative to `chatbot.py`.
- **JSON decode error:** validate commas, quotes, brackets, and ensure the top-level key is `intents`.
- **No useful match:** add representative phrasings to the correct intent and test them. Do not lower the threshold blindly; it increases false matches.
- **Old experiment asks for `.pkl` files or NLTK downloads:** you launched a historical file. Use `streamlit run app.py` from the repository root.
- **PowerShell blocks virtualenv activation:** use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for the current PowerShell process, or invoke `.\.venv\Scripts\python.exe` directly without activating.

## Deployment and Working Link

There is no verified live demo URL yet. A GitHub repository URL is not a deployed app URL, so do not label one as a demo.

To deploy the current app on Streamlit Community Cloud:

1. Push the project to the public GitHub repository and confirm `app.py`, `chatbot.py`, `intents.json`, and `requirements.txt` are on the deployment branch.
2. Open the [Streamlit Community Cloud deploy page](https://share.streamlit.io/deploy?repository=LuckyNawale%2FEcoGenieBot&branch=main&mainModule=app.py) and sign in/connect GitHub if prompted.
3. Select `LuckyNawale/EcoGenieBot`, branch `main`, and main file `app.py`, then deploy.
4. Wait for the build to finish and test the greeting, a known sustainability question, and the fallback on the hosted page.
5. Copy the URL assigned by Streamlit and replace the “not deployed yet” line in `README.md` with that tested URL.

Deployment requires signing into your own GitHub/Streamlit account; this workspace cannot create or verify that hosted URL on your behalf. Streamlit's free-tier availability and limits can change.

## Resume Wording

Possible concise bullet, only if it accurately reflects your contribution:

> Built a sustainability-focused chatbot prototype using Python, Streamlit, and scikit-learn, matching user questions to JSON-defined intents with TF-IDF and cosine similarity and returning a fallback for low-similarity input.

Do not claim an accuracy percentage, production usage, live data integration, or an LLM unless you independently verify that work and can demonstrate it. Confirm the internship date and distinguish your individual contribution from team work.