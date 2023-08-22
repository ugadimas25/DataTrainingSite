import uuid  # Import the uuid module to generate UUIDs
import streamlit as st

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_data_ewkb' not in st.session_state:
    st.session_state.user_data_ewkb= None

print(st.session_state.user_id)

def id_call_generator():
    if st.session_state.user_id is None:
            user_id = str(uuid.uuid4())  # Generate a random UUID
            st.session_state.user_id = user_id  # Store the UUID in session state for subsequent requests

    print("Mau Pulannnnnnnnnnnnnnnnnnnnng")
    print(st.session_state.user_id)

# get id for acces
def get_id_generate():
    # Initialize the session state
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_data_ewkb' not in st.session_state:
        st.session_state.user_data_ewkb= None
    return st.session_state