"""
Out&About Streamlit Application

This code defines a Streamlit application for the Out&About platform. The application includes authentication,
chat functionality, and contact information display. Users can navigate through different pages, and
authenticated users enjoy personalized experiences. The application leverages the Streamlit option_menu and
authentication components, creating a seamless and user-friendly interface.
"""

# [i]                                                                                            #
# [i] Imports                                                                                    #
# [i]                                                                                            #

import streamlit as st

from streamlit_option_menu import option_menu
from login import authenticate_user
from chat_app import chatbot

def get_session_state():
    """
    Utility function to retrieve the Streamlit session state.
    """
    return st.session_state

class OutAndAboutApp:
    def __init__(self):
        """
        Initialize the OutAndAboutApp class.
        """
        self.session_state = get_session_state()

        # Initialize session state attributes if not present
        if not hasattr(self.session_state, "authentication_status"):
            self.session_state.authentication_status = None
        if not hasattr(self.session_state, "user_info"):
            self.session_state.user_info = None
        if not hasattr(self.session_state, "page"):
            self.session_state.page = "Authentication"

        # New attribute to store authentication data persistently
        if not hasattr(self.session_state, "persistent_authentication_data"):
            self.session_state.persistent_authentication_data = None

    def display_home_page(self):
        """
        Display the Home page content.
        """
        st.title("Out&About 🛩 MAIN PAGE")
        if self.session_state.authentication_status == "authenticated" and self.session_state.user_info is not None:
            st.write(f"Welcome, {self.session_state.user_info['username']}!")
        else:
            st.write("You are not authenticated. Please log in.")

    def display_chat_page(self):
        """
        Display the Chat page content.
        """
        st.title("Out&About 🛩 CHAT")
        if self.session_state.authentication_status == "authenticated" and self.session_state.user_info is not None:
            st.write(f"Welcome to the chat, {self.session_state.user_info['username']}!")
            # Call the initialize_chatbot function
            chatbot(self.session_state)
        else:
            st.write("You are not authenticated. Please log in.")

    def display_contact_page(self):
        """
        Display the Contact page content.
        """
        st.title("Out&About 🛩 CONTACT")
        if self.session_state.authentication_status == "authenticated" and self.session_state.user_info is not None:
            st.write(f"Contact us, {self.session_state.user_info['username']}!")
        else:
            st.write("You are not authenticated. Please log in.")

    def display_authentication_page(self):
        """
        Display the Authentication page content.
        """
        # Check if the user is already authenticated
        if self.session_state.authentication_status == "authenticated" and self.session_state.user_info is not None:
            st.title("You are already authenticated!")
            st.markdown(
                """
                <div style="background-color: #4CAF50; padding: 20px; border-radius: 10px; color: white;">
                    <h2>Your Authentication Data</h2>
                    <pre>{}</pre>
                </div>
                """.format(self.session_state.user_info),
                unsafe_allow_html=True
            )
        else:
            # Your authentication content goes here
            submit_button, user_info = authenticate_user()

            # If the form is submitted, perform authentication
            if submit_button:
                if user_info:
                    self.session_state.user_info = user_info
                    self.session_state.authentication_status = "authenticated"
                    
                    # Store the username in the session_state
                    self.session_state.username = user_info['username']
                    
                    # Display a creative success message
                    st.success(f"🎉 Welcome, {user_info['username']}! You are now authenticated!")

                    # Add celebratory balloons
                    st.balloons()

                    # Store the authentication data in the session_state object
                    self.session_state.authentication_data = user_info

                    # Display the authentication data in the authentication page
                    st.write(f"Your authentication data: {user_info}")

                else:
                    # Handle the case where authentication fails
                    st.warning("Authentication failed. Please check your credentials.")

    def run(self):
        """
        Run the OutAndAboutApp application.
        """
        st.set_page_config(page_title="Out&About", page_icon="✈️", layout="wide")

        # Display the option_menu without setting the default
        selected_option = option_menu(
            menu_title=None,
            options=["Authentication", "Home", "Chat", "Contact"],
            icons=["unlock", "house", "chat-dots", "envelope"],
            orientation="horizontal",
            styles={
                # Container styling
                "container": {"padding": "0!important", "background-color": "#222", "color": "#fff"},
            },
        )

        # Store the selected option in session_state
        self.session_state.page = selected_option

        # Display content based on the selected page
        if selected_option == "Home":
            self.display_home_page()
        elif selected_option == "Chat":
            self.display_chat_page()
        elif selected_option == "Contact":
            self.display_contact_page()
        else:
            self.display_authentication_page()


if __name__ == "__main__":    
    app = OutAndAboutApp()
    app.run()