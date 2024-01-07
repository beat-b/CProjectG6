# [i]                                                                                            #
# [i] Imports                                                                                    #
# [i]                                                                                            #
from openai import OpenAI
from util import local_settings
import pickle


# [i]                                                                                            #
# [i] OpenAI API                                                                                 #
# [i]                                                                                            #


class GPT_Helper:
    def __init__(self, OPENAI_API_KEY: str, system_behavior: str = "", model: str = "gpt-3.5-turbo"):
        """
        Initialize the GPT_Helper class.

        Parameters:
            OPENAI_API_KEY (str): API key for OpenAI.
            system_behavior (str): System behavior message to be included.
            model (str): GPT model to use (default is "gpt-3.5-turbo").
        """
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    def get_completion(self, prompt: str, temperature: int = 0) -> str:
        """
        Get completion from the GPT model.

        Parameters:
            prompt (str): User prompt for the model.
            temperature (int): Temperature parameter for randomness (default is 0).

        Returns:
            str: Completed message from the model.
        """
        self.messages.append({"role": "user", "content": prompt})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content
            }
        )

        return completion.choices[0].message.content

# [i]                                                                                            #
# [i] ReviewChatBot                                                                               #
# [i]                                                                                            #

class ReviewChatBot:
    """
    Generate a response using Language Models (LLMs).
    """

    def __init__(self, system_behavior: str):
        """
        Initialize the ReviewChatBot class.

        Parameters:
            system_behavior (str): System behavior message to be included.
        """
        self._system_behavior = system_behavior
        self._username = None

        self.engine = GPT_Helper(
            OPENAI_API_KEY=local_settings.OPENAI_API_KEY,
            system_behavior=system_behavior
        )

    def set_username(self, username: str) -> None:
        """
        Set the username for the chatbot.

        Parameters:
            username (str): User's username.
        """
        self._username = username

    def generate_response(self, message: str) -> str:
        """
        Generate a response for the given message.

        Parameters:
            message (str): User's input message.

        Returns:
            str: Chatbot's response.
        """
        user_message = f"{self._username}: {message}" if self._username else message

        response = self.engine.get_completion(user_message)

        return response

    def __str__(self) -> str:
        """
        Return a string representation of the ReviewChatBot instance.

        Returns:
            str: String representation.
        """
        shift = "   "
        class_name = str(type(self)).split('.')[-1].replace("'>", "")

        return f"🤖 {class_name}."
    
    @property
    def memory(self) -> list:
        """
        Get the conversation history.

        Returns:
            list: List of messages in the conversation.
        """
        return self.engine.messages

    @property
    def system_behavior(self) -> str:
        """
        Get the system behavior.

        Returns:
            str: System behavior message.
        """
        return self._system_behavior

    @system_behavior.setter
    def system_behavior(self, system_config: str) -> None:
        """
        Set the system behavior.

        Parameters:
            system_config (str): New system behavior message.
        """
        self._system_behavior = system_config
