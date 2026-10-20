"""Train the EcoGenieBot intent matcher from the checked-in dataset."""

import json
import random
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class EcoGenieBot:
    """Match user messages to intent examples with TF-IDF similarity."""

    def __init__(self, intents_path=None, confidence_threshold=0.3):
        dataset_path = Path(intents_path) if intents_path else Path(__file__).with_name("intents.json")
        with dataset_path.open(encoding="utf-8") as dataset_file:
            data = json.load(dataset_file)

        self.intents = data["intents"]
        self.confidence_threshold = confidence_threshold
        self.patterns = []
        self.tags = []
        self.responses_by_tag = {}

        for intent in self.intents:
            responses = intent.get("responses", intent.get("response", []))
            if isinstance(responses, str):
                responses = [responses]
            if not responses:
                continue

            tag = intent["tag"]
            self.responses_by_tag[tag] = responses
            for pattern in intent.get("patterns", []):
                self.patterns.append(self._preprocess(pattern))
                self.tags.append(tag)

        if not self.patterns:
            raise ValueError("The intents dataset must contain at least one pattern with a response.")

        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.pattern_vectors = self.vectorizer.fit_transform(self.patterns)

    @staticmethod
    def _preprocess(text):
        return re.sub(r"[^a-z0-9\s]", " ", text.lower()).strip()

    def respond(self, message):
        """Return a matching intent response or a clarification prompt."""
        normalized_message = self._preprocess(message)
        if not normalized_message:
            return "Please enter a question about sustainability or green technology."

        message_vector = self.vectorizer.transform([normalized_message])
        scores = cosine_similarity(message_vector, self.pattern_vectors).ravel()
        best_match = scores.argmax()
        if scores[best_match] < self.confidence_threshold:
            return "I'm not sure I understood. Try asking about sustainability or green technology."

        tag = self.tags[best_match]
        return random.choice(self.responses_by_tag[tag])
