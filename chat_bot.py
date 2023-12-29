"""
ChatBot classes
"""
from openai import OpenAI
from util import local_settings

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import ConversationalRetrievalChain

# [i]                                                                                            #
# [i] OpenAI API                                                                                 #
# [i]                                                                                            #

class GPT_Helper:
    def __init__(self, OPENAI_API_KEY: str, system_behavior: str="", model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.messages = []
        self.model = model
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)  # Add this line

        if system_behavior:
            self.messages.append({
                "role": "system",
                "content": system_behavior
            })

    def load_csv_data(self, file_path, encoding="utf-8", csv_args={'delimiter': ','}):
        loader = CSVLoader(file_path=file_path, encoding=encoding, csv_args=csv_args)
        return loader.load()

    def create_embeddings(self, text_chunks):
        print("Text Chunks:", text_chunks)
        print("Type of Text Chunks:", type(text_chunks))

        embeddings = OpenAIEmbeddings()
        return embeddings.embed_documents(text_chunks)

    def build_faiss_index(self, text_chunks, embeddings):
        return FAISS.from_embeddings(text_chunks, embeddings)

    def search_similar_places(self, query, k=3):
        return self.faiss_index.similarity_search(query, k)

    def get_completion_with_data(self, prompt, temperature=0):
        # Load CSV data, create embeddings, and build FAISS index
        data = self.load_csv_data("./data/cleanTripLisbon.csv")
        text_chunks = self.text_splitter.split_documents(data)
        string_list = [str(item) for item in text_chunks]
        embeddings = self.create_embeddings(string_list)
        # self.faiss_index = self.build_faiss_index(text_chunks,embeddings)

        # Append user prompt and perform completion
        self.messages.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=temperature,
        )
        # Append assistant response
        self.messages.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content
            }
        )

        return completion.choices[0].message.content

# [i]                                                                                            #
# [i] PizzaChatBot                                                                               #
# [i]                                                                                            #

class PizzaChatBot:
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
        response = self.engine.get_completion_with_data(user_message)

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