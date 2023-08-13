import requests
import streamlit as st
from streamlit_lottie import st_lottie
import numpy as np
from PIL import Image
import base64
import re


def app():
    
    show_title = False  # Change this value based on your condition
    if show_title:
        st.title("Home")
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
            

    st.title("Welcome To Training Site Data Repository!!!")
    st.markdown(
        """
    A [streamlit](https://streamlit.io) app template for geospatial applications based on [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu). 
    To create a direct link to a pre-selected menu, add `?page=<app name>` to the URL, e.g., `?page=upload`.
    https://share.streamlit.io/giswqs/streamlit-template?page=upload

    """
    )
    #Find more emoji here: https://www.webfx.com/tools/emoji-cheat-sheet/
    # st.set_page_config(page_title="My Webpage", page_icon=":tada", layout="wide")
   

    def load_lottieurl(url):
        r =requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()

    #----LOAD ASSETS----
    lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")

    #----HEADER SECTION----
    with st.container():
        left_column1, right_column1 = st.columns(2)
        with left_column1:
            st.subheader("Hi, I am Fakhry :wave")
            st.header("A Surveyor and trader cocoa product From Indonesia")
            st.write("I am passionate to learn something new and become more productive")
            st.write("[My Project](https://mashaecocoa.com/)")
        
        with right_column1:

            # Generate HTML code to display the image
            image_path = "https://i.ibb.co/1JK7JbN/Home-Background1.png"
            image_html = f'<img src="{image_path}" alt="Image" class="no-right-click">'

            # Generate CSS code to disable right-click
            css = '''
            <style>
                .no-right-click {
                    pointer-events: none;
                }
            </style>
            '''

            # Display the image and apply the CSS
            st.markdown(image_html + css, unsafe_allow_html=True)


    #----WHAT I DO----
    with st.container():
        st.write("---")
        left_column2, right_column2 = st.columns(2)
        with left_column2:
            st.header("What I do")
            st.write("##")
            st.write(
                """
                On my social media I am advertising for product:
                - Food and Beverage
                - House
                - Animal
                - Gadget
                """
            )
            st.write("[Social Media (IG) >](https://www.instagram.com/mashaecocoa/)")
        with right_column2:
            st_lottie(lottie_coding, height=300, key="coding")


    # container tutorial penggunaan web Youtube
    with st.container():
        st.write("---")
        left_column3, right_column3 = st.columns(2)
        with left_column3:
            st.title("Embedding YouTube Video in Streamlit")

            # YouTube video URL
            youtube_url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE'

            # Display the video
            st.video(youtube_url)
        with right_column3:
            st.write("This Video Explain more about this website")
           

    # container tutorial penggunaan web PDF
    with st.container():
        def displayPDF(file):
        # Opening file from file path
            with open(file, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')

            # Embedding PDF in HTML
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

            # Displaying File
            st.markdown(pdf_display, unsafe_allow_html=True)

        # Example usage with "hww" as the file path:
        file_path = "App/Dsign Repository.pdf"  # Replace "hww" with the actual file path to your PDF file
        displayPDF(file_path)

                    

