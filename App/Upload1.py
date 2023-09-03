import streamlit as st
import psycopg2
import openpyxl
from datetime import datetime
import geocoder
from App.login import get_session_state
import uuid
import re


kelas_tutupan_lahan_options ={
    "Other": "",
    "Sawah": "Sawah",
    "Ladang, tegal, atau huma": "Ladang, tegal, atau huma",
    "Perkebunan": "Perkebunan",
    "Hutan lahan kering": "Hutan lahan kering",
    "Hutan lahan basah": "Hutan lahan basah",
    "Semak dan belukar": "Semak dan belukar",
    "Padang rumput, alang-alang, dan sabana": "Padang rumput, alang-alang, dan sabana",
    "Rumput rawa": "Rumput rawa",
    "Lahan terbangun": "Lahan terbangun",
    "Lahan tidak terbangun": "Lahan tidak terbangun",
    "Danau atau waduk": "Danau atau waduk",
    "Rawa": "Rawa",
    "Sungai": "Sungai",
    "Anjir pelayaran": "Anjir pelayaran",
    "Terumbu karang": "Terumbu karang"
    

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
            database="postgres",
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
        image_data VARCHAR,
        admin_note TEXT,
        FOREIGN KEY (id_users) REFERENCES users(id)
        );
        '''
        cursor.execute(create_table_query)
        conn.commit() 
        
        cursor.close()
        conn.close()

        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Execute a query to check if data exists in the database
            query = "SELECT COUNT(*) FROM spasial_input_user WHERE latitude = %s AND longitude = %s AND date = %s"
            cursor.execute(query, (latitude, longitude, selected_date))
            result1 = cursor.fetchone()

            query2 = "SELECT COUNT(*) FROM spasial_data_training_site WHERE latitude = %s AND longitude = %s AND date = %s"
            cursor.execute(query2, (latitude, longitude, selected_date))
            result2 = cursor.fetchone()

            data_exists1 = result1[0] > 0  # Check if count is greater than 0
            data_exists2 = result2[0] > 0  # Check if count is greater than 0


            cursor.close()
            conn.close()
            if data_exists1 == 0 and data_exists2 == 0:
                if locationgeoAPI:
                    print("Location: " + locationgeoAPI)
                    if latitude is not None and longitude is not None and geom is not None and selected_date is not None and kelas_tutupan_lahan is not "Other":
                        if insert_kelas_tutupan_lahan_manual(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI):
                            st.success("Spatial data inserted successfully.")
                        else:
                            st.error("Error occurred during spatial data inserted. Please try again.")
                    else:
                        st.warning("Pastikan kelas tutupan lahan tidak 'other' dan semua data input tidak 'none'")
                else:
                    st.warning("Location info not available.")
            else:
                st.warning("Data sudah pernah di input oleh pengguna, tolong gunakan data lainnya")

            return True
        except Exception as e:  
            print("Error:", e)
        return False  # Return False if an error occurs during the check         
    
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
    image_data VARCHAR,
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

    import_result = {'success': True, 'warnings': []} 
     
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
        
        try:
            conn = create_connection()
            cursor = conn.cursor()

            # Execute a query to check if data exists in the database
            query = "SELECT COUNT(*) FROM spasial_input_user WHERE latitude = %s AND longitude = %s AND date = %s"
            cursor.execute(query, (latitude, longitude, selected_date))
            result1 = cursor.fetchone()

            query2 = "SELECT COUNT(*) FROM spasial_data_training_site WHERE latitude = %s AND longitude = %s AND date = %s"
            cursor.execute(query2, (latitude, longitude, selected_date))
            result2 = cursor.fetchone()

            data_exists1 = result1[0] > 0  # Check if count is greater than 0
            data_exists2 = result2[0] > 0  # Check if count is greater than 0


            cursor.close()
            conn.close()
            if data_exists1 == 0 and data_exists2 == 0:
                if locationgeoAPI:
                    print("Location: " + locationgeoAPI)
                    if latitude is not None and longitude is not None and geom is not None and selected_date is not None and kelas_tutupan_lahan is not "Other":
                        if insert_kelas_tutupan_lahan_exel(id_users, kelas_tutupan_lahan, latitude, longitude, geom, selected_date, locationgeoAPI):
                            st.success("Spatial data inserted successfully.")
                        else:
                            st.error("Error occurred during spatial data inserted. Please try again.")
                    else:
                        import_result['warnings'].append(f"Pastikan kelas tutupan lahan tidak 'other' dan semua data input tidak 'none' untuk baris: {row}")
                else:
                    import_result['warnings'].append(f"Location info not available for row: {row}")
            else:
                import_result['warnings'].append(f"Data sudah pernah di input oleh pengguna, tolong gunakan data lainnya untuk baris: {row}")

        except Exception as e:  
            print("Error:", e)
            import_result['success'] = False  # Set success to False if an error occurs
            return import_result  # Return if an error occurs during the check    

    if len(import_result['warnings']) > 0:
        import_result['success'] = False  # Set success to False if there are warnings
        print (import_result)
    return import_result
    
    cursor.close()
    conn.close()
    # Close the workbook
    workbook.close()
    

# Streamlit app
def Excel():
    st.header('Import Excel to PostgreSQL')

    # File uploader for Excel file
    excel_file = st.file_uploader('Upload Excel File', type=['xlsx'])

    if excel_file is not None:
        # Check if the user clicks the "Import" button
        if st.button('Import'):
            # Call the function to import Excel data to PostgreSQL
            import_result = import_excel_to_postgres(excel_file)

            if import_result['success']:
                st.success('Data imported successfully!')
            else:
                for warning in import_result['warnings']:
                    st.warning(warning)
                st.error('Error occurred during data import. Please try again.')



# Main Program
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

    st.title("Upload")
    
    # Create a selectbox with some options
    selected_option = st.selectbox('Select an option', ['Manual', 'Excel', 'Option 3'])

    if selected_option == 'Manual':
        input_upload()
    
    if selected_option == 'Excel':
        Excel()



