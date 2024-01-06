# [i]                                                                                            #
# [i] Imports                                                                                    #
# [i]                                                                                            #

import time
import streamlit as st
import os
import pickle
import tempfile

from chat_bot import AttractionBot
from prompt_list import *
from langchain.document_loaders import CSVLoader
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
#from util import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader

# Load environment variables
#load_dotenv()

# Define the path for FAISS database
DB_FAISS_PATH = 'vectorstore/db_faiss'


"""

Streamlit ChatBot Application

This code defines a Streamlit application for a chatbot. The chatbot integrates with a conversational retrieval chain,
handles PDF and CSV file uploads, and provides a user interface for interacting with the chatbot.

"""

def chatbot(session_state):
    """
    Initialize the chatbot and UI components.
    """
    def initialize() -> None:
        with st.expander("Bot Configuration"):
            # Allow the user to select a predefined prompt
            selected_prompt_name = st.selectbox(label="Select Prompt", options=prompt_names)
            session_state.selected_prompt_name = selected_prompt_name  # Store selected prompt in session state

            # Use the selected prompt name to retrieve the corresponding prompt text
            selected_prompt_text = prompt_dict[selected_prompt_name]["prompt"]
            st.session_state.system_behavior = st.text_area(
                label="Prompt",
                value=selected_prompt_text
            )

            # Retrieve the username from session_state
            st.session_state.username = st.session_state.username

            # Initialize or update the chatbot with the current system behavior and username
            if "chatbot" not in st.session_state or st.session_state.chatbot.system_behavior != st.session_state.system_behavior:
                st.session_state.chatbot = AttractionBot(st.session_state.system_behavior)
                st.session_state.chatbot.set_username(st.session_state.username)

        with st.sidebar:
            st.markdown(
                f"ChatBot in use: <font color='cyan'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
            )


        """

        PDF file uploader

        """
        pdf = st.file_uploader("Upload a PDF file", type="pdf")
        if pdf is not None:
            # Read the PDF file and extract text
            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Split the text into chunks using RecursiveCharacterTextSplitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)

            # Generate a unique name for storing embeddings based on the PDF file name
            store_name = pdf.name[:-4]

            # Check if embeddings are already stored, if not, create and store them
            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl", "rb") as f:
                    VectorStore = pickle.load(f)
            else:
                # Create embeddings using Sentence Transformers
                embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
                VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
                with open(f"{store_name}.pkl", "wb") as f:
                    pickle.dump(VectorStore, f)

            # Allow the user to input a question about the PDF file
            query = st.text_input("Ask questions about your PDF file:")

            # If a question is provided, perform similarity search using FAISS
            if query:
                docs = VectorStore.similarity_search(query=query, k=3)

                # Load OpenAI language model and question-answering chain
                llm = OpenAI()
                chain = load_qa_chain(llm=llm, chain_type="stuff")

                # Run the question-answering chain and display the response
                with get_openai_callback() as cb:
                    response = chain.run(input_documents=docs, question=query)
                    print(cb)
                st.write(response)
        
        """
        
        CSV file uploader

        """

        # CSV file uploader in the sidebar
        uploaded_csv = st.sidebar.file_uploader("Upload CSV", type="csv")

        # Handle file upload
        if uploaded_csv:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(uploaded_csv.getvalue())
                tmp_file_path = tmp_file.name

            # Load CSV data using CSVLoader
            loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={'delimiter': ','})
            data = loader.load()

            # Create embeddings using Sentence Transformers
            embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', model_kwargs={'device': 'cpu'})

            # Create a FAISS vector store and save embeddings
            db = FAISS.from_documents(data, embeddings)
            db.save_local(DB_FAISS_PATH)

            # Create a conversational chain
            chain = ConversationalRetrievalChain.from_llm(llm=OpenAI(temperature=0), retriever=db.as_retriever())

            # Function for conversational chat
            def conversational_chat(query):
                result = chain({"question": query, "chat_history": st.session_state['history']})
                st.session_state['history'].append((query, result["answer"]))
                return result["answer"]

            # Initialize chat history
            if 'history' not in st.session_state:
                st.session_state['history'] = []

            # Initialize messages
            if 'generated' not in st.session_state:
                st.session_state['generated'] = ["Hello! Ask me about " + uploaded_csv.name + " 🤗"]

            if 'past' not in st.session_state:
                st.session_state['past'] = ["Hey! 👋"]

            response_container = st.container()
            container = st.container()

            # User input form
            with container:
                with st.form(key='my_form', clear_on_submit=True):
                    user_input = st.text_input("Query:", placeholder="Talk to csv data 👉 (:", key='input')
                    submit_button = st.form_submit_button(label='Send')

                # If user submits a question, perform conversational chat
                if submit_button and user_input:
                    output = conversational_chat(user_input)
                    st.session_state['past'].append(user_input)
                    st.session_state['generated'].append(output)

            # Display chat history
            if st.session_state['generated']:
                with response_container:
                    for i in range(len(st.session_state['generated'])):
                        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                        message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")

    def display_history_messages():
        """
        Display chat history messages.
        """
        for message in session_state.chatbot.memory:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    def display_user_msg(message: str):
        """
        Display user message.
        """
        with st.chat_message("user", avatar="😎"):
            st.markdown(message)

    def display_assistant_msg(message: str, animated=True):
        """
        Display assistant message.
        """
        if animated:
            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()

                full_response = ""
                for chunk in message.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message)

    # List of prompt names
    prompt_names = [
        "Explore Lisbon ChatBot", "Explore a specific area", "Personalized Recommendations", "Weather Consideration",
        "Architectural Wonders", "Lisbon by Night"
    ]

    # Dictionary to map prompt names to their corresponding prompts
    prompt_dict = {
        "Explore Lisbon ChatBot": exploring_lisbon,
        "Explore a specific area": exploring_area,
        "Personalized Recommendations": personalized_recommendations,
        "Weather Consideration": weather_consideration,
        "Architectural Wonders": architectural_wonders,
        "Lisbon by Night": lisbon_by_night
    }

    # Initialize the chatbot
    initialize()

    # Display all messages
    display_history_messages()

    if prompt := st.chat_input("Type your request..."):
        # user sends a message and we display the message
        display_user_msg(message=prompt)

        # chatBot generates the response
        assistant_response = session_state.chatbot.generate_response(message=prompt)

        # Display chatBot response
        display_assistant_msg(message=assistant_response)

        # After all the chat interactions
        with st.sidebar:
            st.text("Memory")
            st.write(session_state.chatbot.memory)
