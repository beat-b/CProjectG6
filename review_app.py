"""
Review to Rating Chat
    ✅ Chat User and Assistant
    ✅ Get Rating from Review using a model
"""
# [i]                                                                                            #
# [i] Imports                                                                                    #
# [i]                                                                                            #

import time
import streamlit as st
import os
import pickle
import tempfile

from review_bot import ReviewChatBot


def reviewbot(session_state):
    """
    Initialize the chatbot and UI components.
    """
    def initialize() -> None:
        # Omit the expander and directly set the prompt name
        selected_prompt_name = prompt_names[0]  # Assuming you have only one prompt
        session_state.selected_prompt_name = selected_prompt_name  # Store selected prompt in session state
        selected_prompt_text = prompt_dict[selected_prompt_name]["prompt"]
        st.session_state.system_behavior = selected_prompt_text

        # Retrieve the username from session_state
        st.session_state.username = st.session_state.username

        # Initialize or update the chatbot with the current system behavior and username
        if "chatbot" not in st.session_state or st.session_state.chatbot.system_behavior != st.session_state.system_behavior:
            st.session_state.chatbot = ReviewChatBot(st.session_state.system_behavior)
            st.session_state.chatbot.set_username(st.session_state.username)

        with st.sidebar:
            st.markdown(
                f"ChatBot in use: <font color='cyan'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
            )

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
    prompt_names = ["Review to Rating"]

    # Review Prompt
    review_prompt = {
    "name": "Rating ChatBot",
    "prompt": """
        TASK:
        You are a chat bot that asks the user for their review and returns a rating.

        PROCESS:

        Step 1: Greet the user like "Hello + username, welcome to RatingBot, here to help you make sense of reviews and provide personalized ratings."
        ATTENTION: Please do not display + username, you need to put the username that is provided in the authentication page.

        Step 2: Don\'t let them answer and ask for their 'Review' which is one of the inputs of the regression model.

        Step 3: Get the rating from the regression model.

        Step 4: Check if the user has more reviews to rate. If yes, go back to step 2.

        Step 5: If the user is done exploring, thank them for using ExploreBot and say goodbye.

        TONE:
        Maintain a personalized and friendly tone throughout the conversation.
        """
        }

    # Dictionary to map prompt names to their corresponding prompts
    prompt_dict = {
        "Review to Rating": review_prompt
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