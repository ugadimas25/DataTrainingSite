import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
import re

def app():

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


    st.title("Contact Us")
    
    sender_email = 'rosasinemo@gmail.com'  # Specify the sender email address here
    receiver_email = 'rosasinemo@gmail.com'  # Specify the receiver email address here
    smtp_server = 'smtp.elasticemail.com'
    smtp_port = 2525
    password = 'CCD9857DF536178B45067E2ADFB917FEA90C'

    # Form inputs
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submit = st.button("Submit")
    
    # Handle form submission
    if submit:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = sender_email
        msg['Subject'] = "Contact Form Submission"
        msg.attach(MIMEText(name, email, message, 'plain'))
        
        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                st.success("Email sent successfully.")
        except Exception as e:
            st.error(f"An error occurred while sending the email: {str(e)}")


