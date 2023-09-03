import streamlit as st
import base64
import psycopg2
from psycopg2 import Error
from App.login import get_session_state
from urllib.request import urlopen

def get_image_url_from_database():
    try:
        session_state = get_session_state()
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )

        # Create a cursor
        cursor = connection.cursor()

        # Execute a SELECT query
        query = "SELECT profile_picture FROM users WHERE id = %s;"
        cursor.execute(query, (session_state.session_data['user_id_login'],))

        # Fetch the result
        image_url = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if  image_url and len(image_url) > 0:
              return image_url[0]  # Extract the image data from the tuple
        else:
            return None

    except (Exception, Error) as e:
        print("Error retrieving image:", e)
        return None

def circle_profile_picture(image_url, container_size=200):
    # Define the custom CSS
    css = f"""
    <style>
    .circle-container {{
        width: {container_size}px;
        height: {container_size}px;
        border-radius: 50%;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #ccc; /* Optional: Add a background color */
    }}
    .circle-image {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }}
    </style>
    """

    # Display the circular profile picture using custom HTML and CSS
    html_code = f"""
    <div class="circle-container">
        <img class="circle-image" src="{image_url}" alt="Profile Picture">
    </div>
    """

    # Render the custom HTML and CSS
    st.sidebar.markdown(css + html_code, unsafe_allow_html=True)

# Example usage
def profile_circle():
    # Retrieve the image URL from the database
    profile_picture_url = get_image_url_from_database()

    # Display the circular profile picture using the retrieved URL
    if profile_picture_url:
        circle_profile_picture(profile_picture_url, container_size=150)
    else:
        st.sidebar.write("No profile picture available.")

    # Your other Streamlit content goes here
    st.sidebar.write("Welcome to my app!")
    st.sidebar.write("Feel free to add more content.")



    