import streamlit as st
import base64

def circle_profile_picture(image_path, container_size=200):
    # Load the profile picture
    with open(image_path, "rb") as f:
        profile_picture = f.read()

    # Encode the image to base64
    profile_picture_base64 = base64.b64encode(profile_picture).decode()

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
        <img class="circle-image" src="data:image/jpeg;base64,{profile_picture_base64}" alt="Profile Picture">
    </div>
    """

    # Render the custom HTML and CSS
    st.sidebar.markdown(css + html_code, unsafe_allow_html=True,)

# Example usage
def profile_circle():
    
    profile_picture_path = "Foto Banner.jpg"
    circle_profile_picture(profile_picture_path, container_size=150)

    # Your other Streamlit content goes here
    st.sidebar.write("Welcome to my app!")
    st.sidebar.write("Feel free to add more content.")





