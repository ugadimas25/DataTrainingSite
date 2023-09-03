import streamlit as st
import psycopg2
import pyotp
import random
import string
from PIL import Image
import re


# session management function to store the authenticated user's information:
def create_session(user):
       session_data = {
           'user_id_login': user[0],
           'username': user[1],
           'password': user[2],
           'status_user': user[15]
           # Add any other relevant user information to the session
       }
       return session_data

# Add a session variable to store the session data:
session_state = st.session_state
if 'session_data' not in session_state:
    session_state.session_data = None
if 'login' not in session_state:
    session_state.login = False


def get_session_state():
    session_state = st.session_state
    if 'session_data' not in session_state:
        session_state.session_data = None
    if 'login' not in session_state:
        session_state.login = False

    return session_state

def create_connection():
        connection = psycopg2.connect(
           host="localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

def login1():

        with open('App/style.css') as f:
                css_styles = f.read()
                
            
                # Define the selector you want to extract styles for
                selector = 'h1'

                # Use regular expression to extract styles for the specific selector
                pattern = rf"{selector}[^{selector}]*{{[^}}]*}}"
                matches = re.findall(pattern, css_styles)

                # Combine the extracted matches into a single string
                extracted_styles = "\n".join(matches)

                st.markdown(f'<style>{extracted_styles}</style>',unsafe_allow_html=True)

        st.title("Login")
        
        username = st.text_input("Username", key="username_input_log")
        password = st.text_input("Password", type="password", key="password_input_log")  

        if st.button("Login"):
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                user = cursor.fetchone()
                print(user)

                if user:
                    session_state.session_data = create_session(user)
                    print(session_state.session_data)
                    st.success("Logged in as {}".format(user[1]))
                    session_state.login = True
                    print (session_state.login)
                    print (session_state.session_data)
                else:
                    st.error("Invalid username or password")
                cursor.close()
                conn.close()

def logout_user():
    # Clear the user session or perform any other necessary tasks
    session_state.session_data = None
    session_state.login = False


