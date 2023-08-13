# import streamlit as st
# import base64
# import psycopg2
# from psycopg2 import Error
# from App.login import get_session_state


# def get_image_from_database():
#     try:
        
#         session_state = get_session_state()
#         # Connect to the PostgreSQL database
#         connection = psycopg2.connect(
#             # host="db.fesgpwzjkedykiwpmatt.supabase.co",
#             # database="postgres",
#             # user="postgres",
#             # password="17agustus2023",
#             # port='5432'
#             host="170.64.133.197",
#             database="postgres",
#             user="postgres",
#             password="admin",
#             port='5432'
#         )

#         # Create a cursor
#         cursor = connection.cursor()

#         # Execute a SELECT query
#         query = "SELECT profile_picture FROM users WHERE id = %s;"
#         cursor.execute(query, session_state.session_data['user_id_login'])

#         # Fetch the result
#         image_data_tuple = cursor.fetchone()
        
#         # Close the cursor and connection
#         cursor.close()
#         connection.close()
#         print ("imaggggggggggggggggggggggggggggggggggggg")
#         if image_data_tuple and len(image_data_tuple) > 0:
#             return image_data_tuple[0]  # Extract the image data from the tuple
#         else:
#             return None

#     except (Exception, Error) as e:
#         print("Error retrieving image:", e)
#         return None

# def circle_profile_picture(image_data, container_size=200):

#     # Encode the image to base64
#     profile_picture_base64 = base64.b64encode(image_data).decode()

#     # Define the custom CSS
#     css = f"""
#     <style>
#     .circle-container {{
#         width: {container_size}px;
#         height: {container_size}px;
#         border-radius: 50%;
#         overflow: hidden;
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         background-color: #ccc; /* Optional: Add a background color */
#     }}
#     .circle-image {{
#         width: 100%;
#         height: 100%;
#         object-fit: cover;
#         border-radius: 50%;
#     }}
#     </style>
#     """

#     # Display the circular profile picture using custom HTML and CSS
#     html_code = f"""
#     <div class="circle-container">
#         <img class="circle-image" src="data:image/jpeg;base64,{profile_picture_base64}" alt="Profile Picture">
#     </div>
#     """

#     # Render the custom HTML and CSS
#     st.sidebar.markdown(css + html_code, unsafe_allow_html=True,)

# # Example usage
# def profile_circle():
    
    
#      # Retrieve the image data from the database (replace with your logic)
#     profile_picture_data = get_image_from_database( )
    
#     # Display the circular profile picture using the retrieved data
#     if profile_picture_data:

#         circle_profile_picture(image_data, container_size=150)
#     else:
#         st.sidebar.write("No profile picture available.")
       

#     # Your other Streamlit content goes here
#     st.sidebar.write("Welcome to my app!")
#     st.sidebar.write("Feel free to add more content.")



import streamlit as st
import base64
import psycopg2
from psycopg2 import Error
from App.login import get_session_state

def get_image_from_database():
    try:
        session_state = get_session_state()
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(
            host="170.64.133.197",
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
        image_data_tuple = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        if image_data_tuple and len(image_data_tuple) > 0:
            return image_data_tuple[0]  # Extract the image data from the tuple
        else:
            return None

    except (Exception, Error) as e:
        print("Error retrieving image:", e)
        return None

def circle_profile_picture(image_data, container_size=200):
    # Encode the image to base64
    profile_picture_base64 = base64.b64encode(image_data).decode()

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
    st.sidebar.markdown(css + html_code, unsafe_allow_html=True)

# Example usage
def profile_circle():
    # Retrieve the image data from the database
    profile_picture_data = get_image_from_database()

    # Display the circular profile picture using the retrieved data
    if profile_picture_data:
        circle_profile_picture(profile_picture_data, container_size=150)
    else:
        st.sidebar.write("No profile picture available.")

    # Your other Streamlit content goes here
    st.sidebar.write("Welcome to my app!")
    st.sidebar.write("Feel free to add more content.")







    