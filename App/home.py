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
            st.write("##")
            st.write("##")
            st.header("Kumpulkan data training site dan berkolaborasi dalam penyediaan data training site")
            
        
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
            st.subheader("Atribut apa saja yang tersedia dan diperlukan?")
            st.write("##")
            st.write(
                """
                - Kelas tutupan lahan
                - Koordinat (Latitude, Longitude)
                - Tanggal pengambilan
                - Foto lokasi data dengan foto GPS
                """
            )
            st.subheader("Ingat login telebih dahulu untuk upload data anda!!!")
        with right_column2:
            st_lottie(lottie_coding, height=300, key="coding")


    # container tutorial penggunaan web Youtube
    with st.container():
        st.write("---")
        left_column3, right_column3 = st.columns(2)
        with left_column3:

            # YouTube video URL
            youtube_url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE'

            # Display the video
            st.video(youtube_url)
        with right_column3:
            st.header("Tutorial Penggunaan WebGIS Repository Data Training Site")
            st.write("This Video Explain more about this website...")
           

    # container tutorial penggunaan web PDF
    with st.container():
        pdf_display = f'<iframe src="https://drive.google.com/file/d/1WNah9QOlIqUzm7IQZYqx13n7CRzfyeBi/preview" width="640" height="480"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

      

    with st.container():
        # Add a section for Excel file download
        st.markdown("## Download Excel File For Upload Data Format Excel")
        file_path_excel = "https://github.com/Fakhrynm/DataTrainingSite/blob/main/App/Tabel%20Input%20Data.xlsx"  # Replace with the actual path to your Excel file
        download_link = f'<a href="{file_path_excel}" download>Click here to download Excel file</a>'
        st.markdown(download_link, unsafe_allow_html=True)

                    

