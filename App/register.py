import streamlit as st
import psycopg2
import pyotp
import random
import string
from PIL import Image
import datetime
import uuid
import re
import logging




# A dictionary of country names and their corresponding flag emojis
country_flags = {
    "Other":"",
    "United States":"🇺🇸",
    "United Kingdom":"🇬🇧",
    "Canada":"🇨🇦",
    "Japan":"🇯🇵",
    "Australia":"🇦🇺",
    "Germany":"🇩🇪",
    "Indonesia":"🇮🇩"
    # Add more country flags as needed
}

#Ditionary of district
district_semarang_city= {
    "Other":"",
    "Tembalang": "Tembalang",
    "Genuk":"Genuk",
    "Candisari":"Candisari"
} 

#Ditionary of sub district
sub_district_tembalang= {
    "Other":"",
    "Tembalang": "Tembalang",
    "Meteseh":"Meteseh",
    "Bulusan":"Bulusan"
} 

#Ditionary of city_regency
city_regency_central_java = {
    "Other":"",
    "Semarang City":"Semarang City",
    "Semarang Regency":"Semarang Regency",
    "Magelang City":"Magelang City"
}

#Dictionary of Province
province_indonesia ={
    "Other": "",
    "West Java": "West Java",
    "Central Java": "Central Java"
}

def create_connection():
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

def is_valid_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def register1():

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

    st.title("Register")

    # Function to generate an id based on username and UUID
    def generate_id(username):
        user_uuid = str(uuid.uuid4()).replace("-", "")
        return f"{username}_{user_uuid}"

    # Function to insert a new user into the "users" table
    def insert_user(username, first_name, last_name, password, birthday, gender, email, country, province, city_regency, district, subdistrict, address, cellphone, status):
        conn = create_connection()
        cursor = conn.cursor()
        print("runnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        try:
            # Generate the id based on username and UUID
            user_id = generate_id(username)

            # Insert the new user into the "users" table
            cursor.execute("INSERT INTO users (id, username, first_name, last_name, password, birthday, gender, email, country, province, city_regency, district, subdistrict, address, cellphone, status) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, username, first_name, last_name, password, birthday, gender, email, country, province, city_regency, district, subdistrict, address, cellphone, status))

            conn.commit() 
            return True# Return True if the insertion is successful
        except Exception as e:
            print("Error inserting user:", e)
            return False# Return False if there is an error during insertion
        finally:
            cursor.close()
            conn.close()
        

    username = st.text_input("Username")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    password = st.text_input("Password", type="password")
    min_date = datetime.date(1900, 1, 1)
    birthday = st.date_input("Birthday", min_value=min_date)
    gender = st.selectbox("Gender", ["Other", "Male", "Female"])
    email = st.text_input("Email")

    
    # Create a list of country names with their flag emojis for the selectbox
    country_names_with_flags = [f"{country_flags[country]} {country}" for country in country_flags.keys()]
    country = st.selectbox("Country", country_names_with_flags)  # Use a selectbox for countries
    country = country.split(" ")[1]  # Extract the selected country name without the flag emoji
    

    if country == "Indonesia":
        province = st.selectbox("Province", list(province_indonesia))
    elif  country == "Other":
        custom_country = st.text_input("Country (Custom)", "")
        if custom_country.strip() != "":
            country = custom_country.strip()
        province = st.text_input("Province")
    else:
        province = st.text_input("Province")

    if province == "Central Java":
        city_regency = st.selectbox ("City/Regency",city_regency_central_java)
    elif  province  == "Other":
        custom_province = st.text_input("Province (Custom)", "")
        if custom_province.strip() != "":
           province = custom_province.strip()
        city_regency= st.text_input("City/Regency")
    else:
        city_regency= st.text_input("City/Regency")
    
    if city_regency == "Semarang City":
        district = st.selectbox ("District",district_semarang_city)
    elif  city_regency == "Other":
        custom_city_regency = st.text_input("City/Regency (Custom)", "")
        if custom_city_regency.strip() != "":
            city_regency = custom_city_regency.strip() 
        district = st.text_input ("District")
    else:
        district = st.text_input ("District")

    if district == "Tembalang":
       subdistrict = st.selectbox ("Sub District",sub_district_tembalang)
    elif  district == "Other":
        custom_district = st.text_input("District (Custom)", "")
        if custom_district.strip() != "":
            district = custom_district.strip() 
        subdistrict = st.text_input ("Sub District")
    else:
        subdistrict = st.text_input ("Sub District")
    
    if  subdistrict == "Other":
        custom_subdistrict = st.text_input("Sub District (Custom)", "")
        if custom_subdistrict.strip() != "":
            subdistrict = custom_subdistrict.strip() 
    

    address = st.text_area("Address")
    
    cellphone = st.text_input("Phone Number")

    status =  ("User") # ("Admin")# 

    if st.button("Register"):
            conn = create_connection()
            cursor = conn.cursor()
             # Create a table to store the data
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                birthday DATE NOT NULL,
                gender VARCHAR(10) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                country VARCHAR(50) NOT NULL,
                province VARCHAR(50) NOT NULL,
                city_regency VARCHAR(50) NOT NULL,
                district VARCHAR(50) NOT NULL,
                subdistrict VARCHAR(50) NOT NULL,
                address TEXT NOT NULL,
                cellphone VARCHAR(20) NOT NULL,
                status VARCHAR(10) NOT NULL,
                profile_picture VARCHAR
            );
            '''
            cursor.execute(create_table_query)
            conn.commit()

            if username.strip() == "":
                st.error("Error: Please provide a username.")
            elif first_name.strip() == "":
                st.error("Error: Please provide your first name.")
            elif last_name.strip() == "":
                st.error("Error: Please provide your last name.")
            elif password.strip() == "":
                st.error("Error: Please provide a password.")
            elif birthday is None:
                st.error("Error: Please provide your birthday.")
            elif email.strip() == "":
                st.error("Error: Please provide an email.")
            elif not is_valid_email(email):
                st.error("Error: Invalid email format.")
                return
            elif country.strip() == "" or country.strip() == "Other":
                st.error("Error: Please select a country.")
            elif province.strip() == "" or province.strip() == "Other":
                st.error("Error: Please provide a province.")
            elif city_regency.strip() == "":
                st.error("Error: Please provide a city/regency.")
            elif district.strip() == "" or district.strip() == "Other":
                st.error("Error: Please provide a district.")
            elif subdistrict.strip() == "" or subdistrict.strip() == "Other":
                st.error("Error: Please provide a sub district.")
            elif address.strip() == "":
                st.error("Error: Please provide an address.")
            elif cellphone.strip() == "":
                st.error("Error: Please provide a phone number.")
            else:
                try:
                    # Check if the username already exists
                    cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
                    count_username = cursor.fetchone()[0]

                    if count_username > 0:
                        st.error("Error: The username is already in use. Please choose a different username.")
                    else:
                        # Check if the email already exists
                        cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                        count_email = cursor.fetchone()[0]

                        if count_email > 0:
                            st.error("Error: The email is already in use. Please choose a different email.")
                        else:                    
                            if insert_user(username, first_name, last_name, password, birthday, gender, email, country, province, city_regency, district, subdistrict, address, cellphone, status) == True:
                                st.success("Registered successfully. Please login.")
                                print (insert_user)
                            else:
                                st.error("Error occurred during registration. Please try again.")
                                print (insert_user)
                except Exception as e:
                    st.error("Error checking username and email:", e)
                finally:
                    cursor.close()
                    conn.close()
            cursor.close()
            conn.close()

