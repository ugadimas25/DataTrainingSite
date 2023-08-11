import streamlit as st
import psycopg2
import pyotp
import random
import string
from PIL import Image

# session management function to store the authenticated user's information:
def create_session(user):
       session_data = {
           'user_id_login': user[0],
           'username': user[1],
           'password': user[2],
           'status_user': user[14]
           # Add any other relevant user information to the session
       }
       return session_data

# Add a session variable to store the session data:
session_state = st.session_state
if 'session_data' not in session_state:
    session_state.session_data = None
if 'login' not in session_state:
    session_state.login = False
# if 'status_user' not in session_state:
#     session_state.status_user = 'Admin'

def get_session_state():
    session_state = st.session_state
    if 'session_data' not in session_state:
        session_state.session_data = None
    if 'login' not in session_state:
        session_state.login = False
    # if 'status_user' not in session_state:
    #     session_state.status_user = 'Admin'
    return session_state


def create_connection():
        connection = psycopg2.connect(
            # host="db.fesgpwzjkedykiwpmatt.supabase.co",
            # database="postgres",
            # user="postgres",
            # password="17agustus2023",
            # port='5432'
            host="170.64.133.197",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

def login1():
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

def logout_user():
    # Clear the user session or perform any other necessary tasks
    session_state.session_data = None
    session_state.login = False


