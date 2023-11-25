"""
Chat
"""
import datetime
import time
import streamlit as st
import openai 
from chat_bot import ChatBot



# [i]                                                                                            #
# [i] Initialize                                                                                 #
# [i]                                                                                            #


def initialize():
    st.title("Out&About 🛩")
    st.markdown("This 24/7 virtual assistant provides uninterrupted support to our users, ensuring that they have access to information and suggestions to explore Lisbon at any time. Our chatbot will make our online presence stronger and improve the visitor experience by giving personalized suggestions, answering questions, and helping with trip planning. At this early stage, our chatbot primarily supports English inquiries, however, we will continually work to expand its language capabilities to serve a wider audience.")
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot()
        # chatBot = ChatBotStatic()


# [i]                                                                                            #
# [i] Display all messages                                                                       #
# [i]                                                                                            #

def display_history_messages():

    # {"role": "assistant", "content": message}

    for message in st.session_state.chatbot.memory:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# [i]                                                                                            #
# [i] Display User messages                                                                      #
# [i]                                                                                            #


def display_user_msg(message: str):
    """
    Display user message in chat message container
    """
    st.session_state.chatbot.memory.append(
        {"role": "user", "content": message}
    )

    with st.chat_message("user", avatar="😎"):
        st.markdown(message)
    

# [i]                                                                                            #
# [i] Display Assistant Message                                                                  #
# [i]                                                                                            #


def display_assistant_msg(message: str):
    """
    Display user message in chat message container
    """
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()  # markdown(message)

    # animate
    full_response = ""
    for chunk in message.split():
        full_response += chunk + " "
        time.sleep(0.05)
        message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)

    st.session_state.chatbot.memory.append(
        {"role": "assistant", "content": message}
    )

# [i]                                                                                            #
# [i] Main                                                                                       #
# [i]                                                                                            #

if __name__ == "__main__":
    # initialize
    initialize()

    # show all messages
    display_history_messages()


    if prompt := st.chat_input("Type your request..."):
        # user send a message and we display the message
        display_user_msg(message=prompt)

        # chatBot generates the response
        assistant_response = st.session_state.chatbot.generate_response(
            message=prompt)

        # Display chatBot response
        display_assistant_msg(message=assistant_response)

        # After all the chat interactions
        with st.sidebar:
            st.title("Answer ☞")

            # input
            user_input = st.text_input("Enter your name", "Your Name")
            
            # Date Input Widget
            date_input = st.sidebar.date_input(
                "Pick a date", datetime.date(2023, 1, 1))  # Create a date input field
            st.sidebar.write("Selected date:", date_input)  # Display the selected date

            # Time Input Widget
            time_input = st.sidebar.time_input(
                "Set a time", datetime.time(12, 00))  # Create a time input field
            st.sidebar.write("Selected time:", time_input)  # Display the selected time

            # Button Widget
            if st.button("Click me"):  # Create a button
                st.write("Button clicked!")  # Display a message when the button is clicked

            # select box
            option = st.selectbox("Choose an option", ["Option 1", "Option 2", "Option 3"])
            st.write("You selected:", option)

            st.text("Memory")
            st.write(st.session_state.chatbot.memory)

        

        