
"""
ChatBot class
"""

import random


# [i] Static ChatBot                                                                               -

class ChatBotStatic:
    """
    ChatBot class
    """

    def __init__(self):
        self.memory = []

    def generate_response(self, message: str):
        """
        Returns a static response
        """
        return "How can I help you?"


# [i] Static ChatBot                                                                               -

class ChatBotRandom:
    """
    ChatBotRandom class provides a simple chatbot that generates random responses.
    """

    def __init__(self):
        self.memory = []

    def generate_response(self, message: str):
        """
        Generates a random response for incoming messages.

        Returns:
            str: A randomly selected response from a list of greeting messages.

        """
        return random.choice(
            [
                "Hello there! How can I assist you today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help?",
            ]
        )


class ChatBot:

    def __init__(self):
        self.memory = []

    def generate_recommendation(self):
        recommendations = [
            "I recommend visiting the historic Bairro Alto.",
            "You might enjoy exploring the Torre de Belém.",
            "Consider checking out the LX Factory for a unique experience."
        ]
        return random.choice(recommendations)

    def generate_weather_response(self):
        weather_responses = [
            "The weather in Lisbon is currently sunny and warm.",
            "Expect some clouds with a chance of rain later in the day."
        ]
        return random.choice(weather_responses)

    def generate_response(self, message: str):
        if any(keyword in message.lower() for keyword in ["recommend", "suggest"]):
            response = self.generate_recommendation()
        elif any(keyword in message.lower() for keyword in ["weather", "forecast"]):
            response = self.generate_weather_response()
        else:
            response = "I'm here to help! If you have any specific questions or need recommendations, feel free to ask."

        return response

    