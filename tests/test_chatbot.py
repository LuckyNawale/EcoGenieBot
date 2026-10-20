import json
import unittest
from pathlib import Path

from chatbot import EcoGenieBot


class EcoGenieBotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bot = EcoGenieBot()
        cls.intents = json.loads(Path("intents.json").read_text(encoding="utf-8"))["intents"]

    def test_matches_a_known_pattern(self):
        intent = next(item for item in self.intents if item["tag"] == "greeting")
        response = self.bot.respond(intent["patterns"][0])
        self.assertIn(response, intent["responses"])

    def test_blank_message_gets_prompt(self):
        self.assertEqual(
            self.bot.respond("!!!"),
            "Please enter a question about sustainability or green technology.",
        )

    def test_unknown_message_gets_clarification(self):
        self.assertEqual(
            self.bot.respond("zzzxqv blorpt"),
            "I'm not sure I understood. Try asking about sustainability or green technology.",
        )

    def test_singular_response_field_is_supported(self):
        intent = next(item for item in self.intents if "response" in item and "responses" not in item)
        self.assertIn(self.bot.respond(intent["patterns"][0]), intent["response"])


if __name__ == "__main__":
    unittest.main()