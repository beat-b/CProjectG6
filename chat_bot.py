"""
ChatBot classes
"""
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders.csv_loader import CSVLoader
from util import local_settings
# from langchain.llms import OpenAI
from openai import OpenAI
from embeddings import embeddings

vectorstore = FAISS.load_local("vectorstore/db_faiss", embeddings)

# [i]                                                                                            #
# [i] OpenAI API                                                                                 #
# [i]                                                                                            #

class GPT_Helper:
    def __init__(self,
        OPENAI_API_KEY: str,
        system_behavior: str="",
        model="gpt-3.5-turbo",
    ):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    # [i] get completion from the model 
    def get_completion(self, prompt, temperature=0):

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
# [i] AttractionBot                                                                               #
# [i]                                                                                            #

class AttractionBot:
    """
    Generate a response by using LLMs.
    """

    def __init__(self, system_behavior: str):
        self._system_behavior = system_behavior
        self._username = None  # Add a private attribute to store the username

        self.engine = GPT_Helper(
            OPENAI_API_KEY=local_settings.OPENAI_API_KEY,
            system_behavior=system_behavior
        )

    def set_username(self, username):
        self._username = username

    def generate_response(self, message: str):
        # Include the username in the message if available
        user_message = f"{self._username}: {message}" if self._username else message
        if user_message:
            vectorstore.similarity_search(user_message)

        response = self.engine.get_completion(user_message)

        # Extract relevant information from the CSV documents
        relevant_responses = []
        for document in vectorstore.similarity_search(user_message):
            relevant_text = document.get("text", None)
            if relevant_text:
                relevant_responses.append(relevant_text)
        # Combine the responses from the LLM and the CSV documents
        response = " ".join(relevant_responses)

        return response
    
    def __str__(self):
        shift = "   "
        class_name = str(type(self)).split('.')[-1].replace("'>", "")

        return f"🤖 {class_name}."

    def reset(self):
        ...
    
    @property
    def memory(self):
        return self.engine.messages

    @property
    def system_behavior(self):
        return self._system_behavior

    @system_behavior.setter
    def system_behavior(self, system_config: str):
        self._system_behavior = system_config
