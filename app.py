import os
import re
import json
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics.pairwise import cosine_similarity
import random
import streamlit as st
import pickle

# Set base path
BASE_PATH = r"C:\Users\lucky\AICTE"

# Add NLTK data path and ensure stopwords are available
NLTK_DATA_PATH = os.path.join(BASE_PATH, "nltk_data")
nltk.data.path.append(NLTK_DATA_PATH)
if not os.path.exists(NLTK_DATA_PATH):
    os.makedirs(NLTK_DATA_PATH)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=NLTK_DATA_PATH)

# Preprocessing function
def preprocess_text(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove digits
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    return " ".join([word for word in words if word not in stop_words])

# Load intents.json
def load_intents(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Error: intents.json file not found!")
        return {"intents": []}

intents = load_intents(os.path.join(BASE_PATH, 'intents.json'))

# Extract patterns and tags
patterns, tags = [], []
for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(preprocess_text(pattern))
        tags.append(intent['tag'])

# Create DataFrame
df = pd.DataFrame({'Pattern': patterns, 'Tag': tags})

# Vectorize text data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['Pattern'])
y = df['Tag']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Logistic Regression model
model = LogisticRegression(max_iter=300)
model.fit(X_train, y_train)

# Save model and vectorizer for reuse
with open(os.path.join(BASE_PATH, 'vectorizer.pkl'), 'wb') as vec_file:
    pickle.dump(vectorizer, vec_file)
with open(os.path.join(BASE_PATH, 'model.pkl'), 'wb') as model_file:
    pickle.dump(model, model_file)

# Evaluate model
y_pred = model.predict(X_test)
print("Model Evaluation:")
print(classification_report(y_test, y_pred))

# Generate chatbot response
def chatbot_response(user_input):
    processed_input = preprocess_text(user_input)
    vectorized_input = vectorizer.transform([processed_input])
    similarity_scores = cosine_similarity(vectorized_input, vectorizer.transform(df['Pattern']))
    max_score_index = np.argmax(similarity_scores)

    if np.max(similarity_scores) < 0.3:
        return "I'm not sure about that. Could you please clarify?"

    matched_tag = df.iloc[max_score_index]['Tag']
    for intent_data in intents['intents']:
        if intent_data['tag'] == matched_tag:
            return random.choice(intent_data['responses'])

    return "I'm sorry, I didn't understand that."

# Streamlit Interface
st.set_page_config(page_title="EcoGenieBot", page_icon="🌱", layout="wide")

# Sidebar Navigation
st.sidebar.markdown("### 🌿 Navigation")
selected_option = st.sidebar.radio(
    "Navigate to:",
    ["🌿 Home", "📚 Resources", "💡 Eco Tips", "❓ Help", "🎮 Quiz Mode"]
)

# Main Interface
if selected_option == "🌿 Home":
    st.title("🌱 EcoGenieBot")
    st.write("EcoGenieBot is your intelligent companion for eco-friendly practices and green technology insights.")
    user_query = st.text_input("Ask EcoGenieBot:", "")
    if user_query:
        response = chatbot_response(user_query)
        st.write(f"**EcoGenieBot:** {response}")

elif selected_option == "📚 Resources":
    st.title("📚 Resources")
    st.markdown("""
        - [Sustainable Living Tips](https://www.sustainable.org/)
        - [Renewable Energy Basics](https://www.energy.gov/)
        - [Climate Change Resources](https://climate.nasa.gov/)
    """)

elif selected_option == "💡 Eco Tips":
    st.title("💡 Eco Tips")
    st.markdown("""
        - 🚰 Save Water: Fix leaks and turn off taps.
        - 💡 Save Energy: Use energy-efficient appliances.
        - 🌱 Plant Trees: Support afforestation projects.
    """)

elif selected_option == "❓ Help":
    st.title("❓ Help")
    st.markdown("""
            
            Getting Started
            Type your question in the chatbox on the Home page and press "Send" to interact with EcoGenieBot.
            Use simple and specific language for better results.
            Navigation Guide

            🌿 Home: Chat with EcoGenieBot for tips and eco-friendly advice.
            📚 Resources: Access curated links to sustainability and climate resources.
            💡 Eco Tips: Quick actionable tips for green living.
                
                Sample Questions

                "What are eco-friendly practices?"
                "How can I reduce energy consumption?"
                "What are the benefits of using public transport?"
                
                Troubleshooting

                Bot is not responding well: Try rephrasing your query for clarity.
                App issues: Refresh the page or check your internet connection.
               
                EcoGenieBot uses AI to provide eco-related advice. Verify critical information through trusted sources.
    """)

elif selected_option == "🎮 Quiz Mode":
    st.title("🎮 EcoGenie Quiz")
    questions = [
        {"question": "What is the most common greenhouse gas emitted by humans?", "options": ["N2O", "CH4", "CO2"], "answer": "CO2"},
        {"question": "Which is a renewable energy source?", "options": ["Coal", "Wind", "Oil"], "answer": "Wind"}
    ]

    score = 0
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        user_answer = st.radio("", q['options'], key=f"q{i}")
        if user_answer == q['answer']:
            score += 1

    if st.button("Submit"):
        st.success(f"Your score: {score}/{len(questions)}")
        if score == len(questions):
            st.balloons()
