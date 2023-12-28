import streamlit as st
import re
from streamlit import session_state


def is_valid_email(email):
    # Use a regular expression to check if the email is in a valid format
    email_regex = r'^\S+@\S+\.\S+$'
    return re.match(email_regex, email) is not None

def authenticate_user():
    st.caption("Sign in with")

    # Custom CSS to style the buttons
    st.markdown(
        """
        <style>
        .stButton>button {
            width: 700px; /* Adjust the width as needed */
            padding: 10px; /* Adjust the padding as needed */
            text-align: center;
            margin: 5px auto; /* Add more space around the buttons */
            display: block;
            color: white; /* Default text color */
        }
        .stButton>button svg {
            margin-right: 10px; /* Adjust space between logo and text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Facebook Login Button with Bootstrap icon
    st.markdown("""
        <div class="stButton">
            <button>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                    <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                </svg>
                Login with Facebook
            </button>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
        <div class="stButton">
            <button>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-google" viewBox="0 0 16 16">
                <path d="M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.792 4.792 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.702 3.702 0 0 0 1.599-2.431H8v-3.08h7.545z"/>
                </svg>
                Login with Google
            </button>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
        <div class="stButton">
            <button>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-apple" viewBox="0 0 16 16">
                <path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43Zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434c-.108-.003-.483-.095-1.254.116-.508.139-1.653.589-1.968.607-.316.018-1.256-.522-2.267-.665-.647-.125-1.333.131-1.824.328-.49.196-1.422.754-2.074 2.237-.652 1.482-.311 3.83-.067 4.56.244.729.625 1.924 1.273 2.796.576.984 1.34 1.667 1.659 1.899.319.232 1.219.386 1.843.067.502-.308 1.408-.485 1.766-.472.357.013 1.061.154 1.782.539.571.197 1.111.115 1.652-.105.541-.221 1.324-1.059 2.238-2.758.347-.79.505-1.217.473-1.282Z"/>
                <path d="M11.182.008C11.148-.03 9.923.023 8.857 1.18c-1.066 1.156-.902 2.482-.878 2.516.024.034 1.52.087 2.475-1.258.955-1.345.762-2.391.728-2.43Zm3.314 11.733c-.048-.096-2.325-1.234-2.113-3.422.212-2.189 1.675-2.789 1.698-2.854.023-.065-.597-.79-1.254-1.157a3.692 3.692 0 0 0-1.563-.434c-.108-.003-.483-.095-1.254.116-.508.139-1.653.589-1.968.607-.316.018-1.256-.522-2.267-.665-.647-.125-1.333.131-1.824.328-.49.196-1.422.754-2.074 2.237-.652 1.482-.311 3.83-.067 4.56.244.729.625 1.924 1.273 2.796.576.984 1.34 1.667 1.659 1.899.319.232 1.219.386 1.843.067.502-.308 1.408-.485 1.766-.472.357.013 1.061.154 1.782.539.571.197 1.111.115 1.652-.105.541-.221 1.324-1.059 2.238-2.758.347-.79.505-1.217.473-1.282Z"/>
                </svg>
                Login with Apple
            </button>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
        <div class="stButton">
            <button>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8"/>
                </svg>
                Login with Github
            </button>
        </div>""", unsafe_allow_html=True)


    # Add separator line and "or continue with" text
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px; margin-bottom: 20px;">
            <span style="width: 30%; display: inline-block; vertical-align: middle; border-top: 1px solid #888; margin-right: 20px;"></span>
            <span style="font-size: 14px; color: #777; display: inline-block; vertical-align: middle;">or continue with</span>
            <span style="width: 30%; display: inline-block; vertical-align: middle; border-top: 1px solid #888; margin-left: 20px;"></span>
        </div>
        """,
        unsafe_allow_html=True)
    
    # Username input field
    username = st.text_input("Username")

    # Email input field
    email = st.text_input("Email")

    # Password input field with type="password"
    password = st.text_input("Password", type="password")

    # Remember Me checkbox
    st.checkbox("Remember Me")

    # Forgot Password link
    st.markdown("[Forgot Your Password?](#)")  # Add your link or logic here

    # "Sign in" button
    submit_button = st.button("Sign in")

    # If the form is submitted, perform input validation and authentication
    if submit_button:
        # Check if email is valid
        if not is_valid_email(email):
            st.warning("Please enter a valid email address.")
            return (submit_button, None)  # Returning a tuple with the submit button and None

        # Check if username is empty
        if not username:
            st.warning("Please enter a username.")
            return (submit_button, None)  # Returning a tuple with the submit button and None

        # Check if password is empty
        if not password:
            st.warning("Please enter a password.")
            return (submit_button, None)  # Returning a tuple with the submit button and None

        # Placeholder logic to identify the user based on email and password.
        # Replace this with your actual backend implementation.
        # For the sake of this example, it returns a hardcoded username.
        user_info = {"username": username, "email": email}        
        return (submit_button, user_info)  # Returning a tuple with the submit button and user info

    return (submit_button, None)  # Returning a tuple with the submit button and None

