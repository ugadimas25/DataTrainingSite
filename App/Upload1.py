import streamlit as st
import psycopg2
import openpyxl
from datetime import datetime
import geocoder
from App.login import get_session_state
import uuid


kelas_tutupan_lahan_options ={
    "Other": "",
    "perairan": "perairan",
    "vegetasi": "vegetasi"
}

# Initialize session_state
session_state = get_session_state()

def get_location_info(latitude, longitude):
    try:
        location = geocoder.osm([latitude, longitude], method='reverse')
        if location.ok:
            location_info = location.address
            return location_info
        else:
            st.error(f"Geocoding failed: {location.status}")
    except Exception as e:
        st.error(f"Error: {e}")
    return None

# Function to generate an id based on kelas penutup lahan and UUID
def generate_id(kelas_tutupan_lahan):
    user_uuid = str(uuid.uuid4()).replace("-", "")
    return f"{kelas_tutupan_lahan}_{user_uuid}"

def create_connection():
        connection = psycopg2.connect(
            host="localhost",
            database="WebGIS TA",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

def input_upload():
    st.header("Insert Spatial Data")

    id_users = session_state.session_data['user_id_login']
    kelas_tutupan_lahan = st.selectbox("Kelas Tutupan Lahan", list(kelas_tutupan_lahan_options))
    # Input fields for spatial data
    latitude = st.number_input("Latitude", format="%.7f", min_value= -90.0, max_value= 90.0, value=0.0)
    longitude = st.number_input("Longitude", format="%.7f", min_value= -180.0, max_value=180.0, value=0.0) 

    # Date input field
    selected_date = st.date_input("Select a Date")

    geom = f"POINT ({longitude} {latitude})" #POINT(longitude latitude)

    # Function to insert a "kelas penutup lahan" manual methode
    def insert_kelas_tutupan_lahan_manual(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI):
        conn = create_connection()
        cursor = conn.cursor()
        print("runnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        print(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI)
        try:
            # Generate the id based on username and UUID
            user_id_for_input = generate_id(kelas_tutupan_lahan)
            print(user_id_for_input )
            # Insert the new user into the "users" table
            cursor.execute("INSERT INTO spasial_input_user ( id_kelas_tutupan_lahan, id_users,kelas_tutupan_lahan,latitude,longitude,geom,date,location) "
                        "VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326), %s, %s)",
                        (user_id_for_input, id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI))

            conn.commit() 
            return True# Return True if the insertion is successful
        except Exception as e:
            print("Error inserting user:", e)
            return False# Return False if there is an error during insertion
        finally:
            cursor.close()
            conn.close()

    # Submit button
    if st.button("Submit"):
        conn = create_connection()
        cursor = conn.cursor()
        locationgeoAPI = get_location_info(latitude, longitude)

        # Insert spatial data into the database
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS spasial_input_user (
        id_kelas_tutupan_lahan VARCHAR PRIMARY KEY NOT NULL,
        id_users VARCHAR NOT NULL,
        kelas_tutupan_lahan VARCHAR NOT NULL,
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        geom GEOMETRY NOT NULL,
        location VARCHAR NOT NULL,
        date DATE NOT NULL,
        image_data BYTEA,
        admin_note TEXT,
        FOREIGN KEY (id_users) REFERENCES users(id)
        );
        '''
        cursor.execute(create_table_query)
        conn.commit() 

        if locationgeoAPI:
            print("Location: " + locationgeoAPI)

            if insert_kelas_tutupan_lahan_manual(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI):
                st.success("Spatial data inserted successfully.")
            else:
                st.error("Error occurred during spatial data inserted. Please try again.")
        else:
            st.warning("Location info not available.")
       

        cursor.close()
        conn.close()

    
def import_excel_to_postgres(excel_file):
    conn = create_connection()
    cursor = conn.cursor()


    # Open the Excel file
    workbook = openpyxl.load_workbook(excel_file)

    # Select the worksheet containing the data
    worksheet_name = 'Sheet1'
    worksheet = workbook[worksheet_name]

    # Specify the column indices for latitude, longitude, and image
    kelas_tutupan_lahan_coloum = 'A'
    latitude_column = 'B'
    longitude_column = 'C'
    date_column = 'D'

    # Get the maximum row number
    max_row = worksheet.max_row


    

    # Insert spatial data into the database
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS spasial_input_user (
    id_kelas_tutupan_lahan VARCHAR PRIMARY KEY NOT NULL,
    id_users VARCHAR NOT NULL,
    kelas_tutupan_lahan VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    geom GEOMETRY NOT NULL,
    location VARCHAR NOT NULL,
    date DATE NOT NULL,
    image_data BYTEA,
    admin_note TEXT,
    FOREIGN KEY (id_users) REFERENCES users(id)
    );
    '''
    cursor.execute(create_table_query)
    conn.commit() 

    # Function to insert a "kelas penutup lahan" manual methode
    def insert_kelas_tutupan_lahan_exel(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI):
        conn = create_connection()
        cursor = conn.cursor()
        print("runnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        print(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI)
        try:
            # Generate the id based on username and UUID
            user_id_for_input = generate_id(kelas_tutupan_lahan)
            print(user_id_for_input )
            # Insert the new user into the "users" table
            cursor.execute("INSERT INTO spasial_input_user ( id_kelas_tutupan_lahan, id_users, kelas_tutupan_lahan, latitude, longitude, geom, date, location) "
                        "VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326), %s, %s)",
                        (user_id_for_input, id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI))

            conn.commit() 
            return True# Return True if the insertion is successful
        except Exception as e:
            print("Error inserting user:", e)
            return False# Return False if there is an error during insertion
        finally:
            cursor.close()
            conn.close()


     

    # Iterate over the rows and insert the data into the database
    for row in range(2, max_row + 1): 
         # Assuming the data starts from row 2
        id_users = session_state.session_data['user_id_login']
        kelas_tutupan_lahan = worksheet[f'{kelas_tutupan_lahan_coloum}{row}'].value
        latitude = worksheet[f'{latitude_column}{row}'].value
        longitude = worksheet[f'{longitude_column}{row}'].value
        selected_date = worksheet[f'{date_column}{row}'].value
        geom = f"POINT ({longitude} {latitude})" #POINT(longitude latitude)
        locationgeoAPI = get_location_info(latitude, longitude)
        
        
        insert_kelas_tutupan_lahan_exel(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI)
        
       
       


    cursor.close()
    conn.close()

    # Close the workbook
    workbook.close()

# Streamlit app
def Excel():
    st.title('Import Excel to PostgreSQL')

    # File uploader for Excel file
    excel_file = st.file_uploader('Upload Excel File', type=['xlsx'])

    if excel_file is not None:
        # Check if the user clicks the "Import" button
        if st.button('Import'):
            # Call the function to import Excel data to PostgreSQL
            import_excel_to_postgres(excel_file)

            st.success('Data imported successfully!')



# Main Program
def app():
    st.title("upload")
    
    # Create a selectbox with some options
    selected_option = st.selectbox('Select an option', ['Manual', 'Excel', 'Option 3'])

    if selected_option == 'Manual':
        input_upload()
    
    if selected_option == 'Excel':
        Excel()



