# EcoGenieBot 🌱🤖

An intent-based AI chatbot focused on environmental awareness and sustainability, developed as part of AICTE internship project in December 2023.

## Overview

EcoGenieBot is an intelligent conversational AI designed to provide information and guidance on environmental topics, sustainability practices, and eco-friendly solutions. The bot uses Natural Language Processing (NLP) to understand user intents and provide relevant responses.

## Features

- Intent-based conversation handling
- Environmental awareness and sustainability guidance
- Natural Language Processing using NLTK
- Web interface using Streamlit
- Machine learning model for intent classification

## Project Structure

```
├── app.py                 # Main Flask application
├── streamlit.py          # Streamlit web interface
├── chatbot.py            # Core chatbot logic
├── intents.json          # Training data with intents and responses
├── model.pkl             # Trained machine learning model
├── vectorizer.pkl        # Text vectorizer for preprocessing
├── notebooks/            # Jupyter notebooks for development
└── docs/                 # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ecogeniebot.git
cd ecogeniebot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Usage

### Running with Streamlit
```bash
streamlit run streamlit.py
```

### Running with Flask
```bash
python app.py
```

## Development

The project was developed through multiple iterations:
- Week 1: Basic chatbot structure and intent recognition
- Week 2: Enhanced NLP processing and response generation
- Week 3: Web interface and deployment preparation

## Technologies Used

- Python
- NLTK (Natural Language Toolkit)
- Scikit-learn
- Streamlit
- Flask
- Pandas
- NumPy

## Contributing

This project was developed as part of an AICTE internship. Feel free to fork and enhance the chatbot's capabilities.

## License

This project is open source and available under the MIT License.

## Author

Lucky Manoj Nawale
AICTE Internship Project - December 2023