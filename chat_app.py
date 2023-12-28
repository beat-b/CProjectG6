import time
import streamlit as st
from chat_bot import PizzaChatBot
from langchain.prompts import PromptTemplate
from prompt_list import *
import pandas as pd


def chatbot(session_state):
    def initialize() -> None:
        with st.expander("Bot Configuration"):
            selected_prompt_name = st.selectbox(label="Select Prompt", options=prompt_names)
            session_state.selected_prompt_name = selected_prompt_name  # Store selected prompt in session state

            # Use the selected prompt name to retrieve the corresponding prompt text
            selected_prompt_text = prompt_templates[selected_prompt_name]
            
            st.session_state.system_behavior = st.text_area(
                label="Prompt",
                value=selected_prompt_text
            )

            # Retrieve the username from session_state
            st.session_state.username = st.session_state.username

            # Initialize or update the chatbot with the current system behavior and username
            if "chatbot" not in st.session_state or st.session_state.chatbot.system_behavior != st.session_state.system_behavior:
                st.session_state.chatbot = PizzaChatBot(st.session_state.system_behavior)
                st.session_state.chatbot.set_username(st.session_state.username)

        with st.sidebar:
            st.markdown(
                f"ChatBot in use: <font color='cyan'>{st.session_state.chatbot.__str__()}</font>", unsafe_allow_html=True
            )

    def display_history_messages():
        for message in session_state.chatbot.memory:
             if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    def display_user_msg(message: str):
        with st.chat_message("user", avatar="😎"):
            st.markdown(message)
            
    def display_assistant_msg(message: str, animated=True):
        """
        Display assistant message
        """

        if animated:
            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()

                # Simulate stream of response with milliseconds delay
                full_response = ""
                for chunk in message.split():
                    full_response += chunk + " "
                    time.sleep(0.05)

                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message)

    # List of prompt names
    prompt_names = [
        "Explore Lisbon ChatBot with User Login", "Explore a specific area", "Personalized Recommendations", "Ratings and Reviews", "Nearby Attractions",
        "Daily Specials", "Weather Consideration", "City Events Navigator", "Architectural Wonders", "Lisbon by Night"
    ]

    # Create individual PromptTemplate instances for each prompt
    exploring_lisbon_template = PromptTemplate.from_template(template=exploring_lisbon["prompt"])
    exploring_area_template = PromptTemplate.from_template(template=exploring_area["prompt"])
    personalized_recommendations_template = PromptTemplate.from_template(template=personalized_recommendations["prompt"])
    ratings_and_reviews_template = PromptTemplate.from_template(template=ratings_and_reviews["prompt"])
    nearby_attractions_template = PromptTemplate.from_template(template=nearby_attractions["prompt"])
    daily_specials_template = PromptTemplate.from_template(template=daily_specials["prompt"])
    weather_consideration_template = PromptTemplate.from_template(template=weather_consideration["prompt"])
    city_events_navigator_template = PromptTemplate.from_template(template=city_events_navigator["prompt"])
    architectural_wonders_template = PromptTemplate.from_template(template=architectural_wonders["prompt"])
    lisbon_by_night_template = PromptTemplate.from_template(template=lisbon_by_night["prompt"])

    # Create a dictionary to map prompt names to their corresponding PromptTemplate instances
    prompt_templates = {
        "Explore Lisbon ChatBot with User Login": exploring_lisbon_template,
        "Explore a specific area": exploring_area_template,
        "Personalized Recommendations": personalized_recommendations_template,
        "Ratings and Reviews": ratings_and_reviews_template,
        "Nearby Attractions": nearby_attractions_template,
        "Daily Specials": daily_specials_template,
        "Weather Consideration": weather_consideration_template,
        "City Events Navigator": city_events_navigator_template,
        "Architectural Wonders": architectural_wonders_template,
        "Lisbon by Night": lisbon_by_night_template
    }

    # Initialize the chatbot
    initialize()

    # Display all messages
    display_history_messages()

    if prompt:= st.chat_input("Type your request..."):
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