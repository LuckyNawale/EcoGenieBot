import streamlit as st
import pickle
import json
import random
from datetime import datetime

# Load vectorizer and model
with open('vectorizer.pkl', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load intents
with open('intents.json', 'r') as file:
    intents = json.load(file)

# Preprocessing function
def preprocess_text(text):
    tokens = text.lower().split()
    return ' '.join(tokens)

# Chatbot response logic
def chatbot_response(user_input):
    processed_input = preprocess_text(user_input)
    vectorized_input = vectorizer.transform([processed_input])
    predicted_intent = model.predict(vectorized_input)[0]

    if predicted_intent == "weather":
        return "Which city's weather would you like to know?"
    elif predicted_intent == "time":
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    else:
        for intent_data in intents:
            if intent_data["tag"] == predicted_intent:
                return random.choice(intent_data["responses"])

# Streamlit app
st.title("EcoGenieBot")
st.write("Ask me anything about green technology, weather, or time!")


user_input = st.text_input("You: ", "")
if user_input:
    response = chatbot_response(user_input)
    st.text_area("EcoGenieBot:", value=response, height=200)
