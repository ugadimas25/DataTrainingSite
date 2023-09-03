import streamlit as st
import psycopg2
from PIL import Image
import io
from App.login import get_session_state
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.parse import urlparse
import os
import uuid



def create_connection():
        connection = psycopg2.connect(
            host="170.64.133.197", #"localhost",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

# Function to delete file to DigitalOcean Spaces fotoprofile
def delete_from_digitalocean_space(space_name, space_file_name):
    # Konfigurasi akun DigitalOcean Spaces
    s3 = boto3.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com',
                    aws_access_key_id='DO00ATNNKV4K77MB29DB', aws_secret_access_key='WeVAgMDRhl2QWxw2cErT+/hPsgf4JzZNRjEXVF7xqnQ')

    try:
        # Delete the file from the Space
        s3.delete_object(Bucket=space_name, Key=f"fotoprofile/{space_file_name}")

        print("File berhasil dihapus dari DigitalOcean Spaces!")
        return True
    except NoCredentialsError:
        print("Tidak ditemukan kredensial yang valid. Pastikan Anda telah mengatur do_access_key_id dan do_secret_access_key.")
        return False

# Function to upload file to DigitalOcean Spaces fotoprofilr
def upload_to_digitalocean_space(file_data, space_name, space_file_name):
   # Konfigurasi akun DigitalOcean Spaces
    s3 = boto3.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com',
                    aws_access_key_id='DO00ATNNKV4K77MB29DB', aws_secret_access_key='WeVAgMDRhl2QWxw2cErT+/hPsgf4JzZNRjEXVF7xqnQ')

    try:
        # Upload the file to the Space in the "data/image" folder
        s3.upload_fileobj(file_data, space_name, f"fotoprofile/{space_file_name}", ExtraArgs={'ACL': 'public-read'})

        print("File berhasil diunggah!")
        return True
    except NoCredentialsError:
        print("Tidak ditemukan kredensial yang valid. Pastikan Anda telah mengatur do_access_key_id dan do_secret_access_key.")
        return False

# Function to delete file to DigitalOcean Spaces data training site
def delete_from_digitalocean_space_dts(space_name, space_file_name):
    # Konfigurasi akun DigitalOcean Spaces
    s3 = boto3.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com',
                    aws_access_key_id='DO00ATNNKV4K77MB29DB', aws_secret_access_key='WeVAgMDRhl2QWxw2cErT+/hPsgf4JzZNRjEXVF7xqnQ')

    try:
        # Delete the file from the Space
        s3.delete_object(Bucket=space_name, Key=f"trainingsiteimage/{space_file_name}")

        print("File berhasil dihapus dari DigitalOcean Spaces!")
        return True
    except NoCredentialsError:
        print("Tidak ditemukan kredensial yang valid. Pastikan Anda telah mengatur do_access_key_id dan do_secret_access_key.")
        return False

# Function to upload file to DigitalOcean Spaces data training site
def upload_to_digitalocean_space_dts(file_data, space_name, space_file_name):
   # Konfigurasi akun DigitalOcean Spaces
    s3 = boto3.client('s3', endpoint_url='https://sgp1.digitaloceanspaces.com',
                    aws_access_key_id='DO00ATNNKV4K77MB29DB', aws_secret_access_key='WeVAgMDRhl2QWxw2cErT+/hPsgf4JzZNRjEXVF7xqnQ')

    try:
        # Upload the file to the Space in the "data/image" folder
        s3.upload_fileobj(file_data, space_name, f"trainingsiteimage/{space_file_name}", ExtraArgs={'ACL': 'public-read'})

        print("File berhasil diunggah!")
        return True
    except NoCredentialsError:
        print("Tidak ditemukan kredensial yang valid. Pastikan Anda telah mengatur do_access_key_id dan do_secret_access_key.")
        return False

def app():
    st.title("Profile")

    # Create a cursor object to execute queries
    session_state = get_session_state()
    conn = create_connection()
    cursor = conn.cursor()

    create_table_query = '''
            CREATE TABLE IF NOT EXISTS spasial_data_training_site (
            id_kelas_tutupan_lahan VARCHAR PRIMARY KEY NOT NULL,
            id_users VARCHAR NOT NULL,
            kelas_tutupan_lahan VARCHAR NOT NULL,
            latitude FLOAT NOT NULL,
            longitude FLOAT NOT NULL,
            geom GEOMETRY NOT NULL,
            location VARCHAR NOT NULL,
            date DATE NOT NULL,
            image_data VARCHAR,
            FOREIGN KEY (id_users) REFERENCES users(id)
            );
            '''
    cursor.execute(create_table_query)
    conn.commit()
   
    with st.container():
        conn = create_connection()
        cursor = conn.cursor()
        
        # Retrieve profile details from the database
        query = "SELECT username, email, first_name, last_name, country, province, city_regency, district, subdistrict, address, cellphone FROM users WHERE id = %s;"
        cursor.execute(query, (session_state.session_data['user_id_login'],))
        user_data = cursor.fetchone()

        if user_data:
            username = user_data[0]
            email = user_data[1]
            first_name = user_data[2]
            last_name = user_data[3]
            country = user_data[4]
            province = user_data[5]
            city_regency = user_data[6]
            district = user_data[7]
            subdistrict = user_data[8]
            address = user_data[9]
            cellphone = user_data[10]

            # Display other profile details
            st.write(f"Username     : {username}")
            st.write(f"Name         : {first_name} {last_name}")
            full_address = f"{address}, {subdistrict}, {district}, {city_regency}, {province}, {country}"
            st.write(f"Full Address : {full_address}")
            st.write(f"Email        : {email}")
            st.write(f"Phone Number : {cellphone if cellphone else 'Not provided'}")

           
        # Create a selectbox with some options
        selected_option = st.selectbox('Select an option for update yor profile', ['No', 'Update Profile'])

        if selected_option == 'Update Profile':  
        
         # Allow the user to update their profile
            st.subheader("Update Profile")
            new_first_name = st.text_input("New First Name", first_name)
            new_last_name = st.text_input("New Last Name", last_name)
            new_email = st.text_input("New Email", email)
            new_address = st.text_input("New Address", address)
            new_subdistrict = st.text_input("New Sub District", subdistrict)
            new_district = st.text_input("New District", district)
            new_city_regency = st.text_input("New City/Regency", city_regency)
            new_province = st.text_input("New Province", province)
            new_country = st.text_input("New Country", country)
            new_cellphone = st.text_input("New Phone Number", cellphone)

            if st.button("Update"):
                # Perform the update query here
                update_query = "UPDATE users SET first_name = %s, last_name = %s, email = %s, address = %s, subdistrict = %s, district = %s, city_regency = %s, province = %s, country = %s, cellphone = %s WHERE id = %s;"
                cursor.execute(update_query, (new_first_name, new_last_name, new_email, new_address, new_subdistrict, new_district, new_city_regency, new_province, new_country, new_cellphone, session_state.session_data['user_id_login']))
                conn.commit()
                st.success("Profile updated successfully!")

    
        # Set up Streamlit app
        st.title("Update Profile Picture")

        # Input for uploading a new profile picture
        new_image = st.file_uploader("Upload New Profile Picture", type=["png", "jpg"])

        # Update button
        if new_image is not None:
            image_extension = new_image.name.split(".")[-1].lower()  # Extract the last part of the name after the dot

            if st.button("Update Profile Picture"):
                # Example usage
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT profile_picture FROM users WHERE id = %s", (session_state.session_data['user_id_login'],))
                name_delete = cursor.fetchone()
                conn.commit()
                cursor.close()
                conn.close()

                if name_delete is not None:
                    space_name = 'tugasakhir'
                    space_file_name_to_delete = name_delete[0]  # Nama file yang ingin dihapus
                    parsed_url = urlparse(space_file_name_to_delete)
                    file_name = os.path.basename(parsed_url.path)
                    print(file_name)
                    
                    # Memanggil fungsi untuk menghapus file dari DigitalOcean Spaces
                    delete_from_digitalocean_space(space_name, file_name)
                
                # Generate a unique ID
                generated_id = str(uuid.uuid4())

                image_name =  f"{session_state.session_data['user_id_login']}{generated_id }.{image_extension}"
                # Upload the new image to DigitalOcean Spaces
                space_name = 'tugasakhir'

                if upload_to_digitalocean_space(new_image, space_name, image_name):
                    # Update the image in the database using SQL UPDATE statement
                    full_url = f"https://tugasakhir.sgp1.cdn.digitaloceanspaces.com/fotoprofile/{image_name}"
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET profile_picture = %s WHERE id = %s", (full_url, session_state.session_data['user_id_login'],))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    # Show a success message
                    st.success("Profile picture updated successfully!")   
     
    with st.container():
        st.write("---")
        # Create a cursor object to execute queries
        st.header("Data that needs validation from admin")
        conn = create_connection()
        cursor = conn.cursor()
    
        # Execute a query to retrieve the data
        query = "SELECT id_kelas_tutupan_lahan, id_users, kelas_tutupan_lahan, latitude, longitude, geom, location, date, image_data, admin_note FROM spasial_input_user WHERE id_users = %s"
        cursor.execute(query, (session_state.session_data['user_id_login'],))
        # Fetch all the rows returned by the query
        data = cursor.fetchall()
           
        for row in data:
            st.write('---')
            # Allow the user to upload a new image
            new_image = st.file_uploader(f"Update Image for ID {row[0]}", type=["png", "jpg"])

            if new_image is not None:
                image_extension = new_image.name.split(".")[-1].lower()  # Extract the last part of the name after the dot

                if st.button("Update Foto Training Site"):
                    # Example usage
                    # Update the image in the database using SQL UPDATE statement
                    id_to_update = row[0]
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT image_data FROM spasial_input_user WHERE id_kelas_tutupan_lahan = %s", (id_to_update,))
                    name_delete = cursor.fetchone()
                    conn.commit()
                    cursor.close()
                    conn.close()

                    if name_delete is not None:
                        space_name = 'tugasakhir'
                        space_file_name_to_delete = name_delete[0]  # Nama file yang ingin dihapus
                        parsed_url = urlparse(space_file_name_to_delete)
                        file_name = os.path.basename(parsed_url.path)
                        print(file_name)
                        
                        # Memanggil fungsi untuk menghapus file dari DigitalOcean Spaces
                        delete_from_digitalocean_space_dts(space_name, file_name)
                    
                    # Generate a unique ID
                    generated_id = str(uuid.uuid4())

                    image_name =  f"{id_to_update}{generated_id }.{image_extension}"
                    print(image_name)
                    # Upload the new image to DigitalOcean Spaces
                    space_name = 'tugasakhir'

                    if upload_to_digitalocean_space_dts(new_image, space_name, image_name):
                        # Update the image in the database using SQL UPDATE statement
                        full_url = f"https://tugasakhir.sgp1.cdn.digitaloceanspaces.com/trainingsiteimage/{image_name}"
                        conn = create_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE spasial_input_user SET  image_data  = %s WHERE id_kelas_tutupan_lahan = %s", (full_url, id_to_update,))
                        conn.commit()
                        cursor.close()
                        conn.close()

                        # Show a success message
                        st.success("Profile picture updated successfully!")   
                

            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 1])

            with col1:
                st.write("Latitude:", row[3])

            with col2:
                st.write("Longitude:", row[4])

            with col3:
                st.write("Location:", row[6])

            with col4:
                st.write("Date:", row[7])

            with col5:
                if row[8] is not None and len(row[8]) > 0:
                    # URL gambar
                    url_gambar = row[8]

                    # Menampilkan gambar
                    st.image(url_gambar, caption= row[2], use_column_width=True)
                else:
                    st.write("No image available")
            
            with col6:
                # Delete button
                if st.button(f"Delete ID {row[0]}"):
                    # Select the image in the database using SQL SELECT statement
                    id_to_update = row[0]
                    conn = create_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT image_data FROM spasial_input_user WHERE id_kelas_tutupan_lahan = %s", (id_to_update,))
                    name_delete = cursor.fetchone()
                    conn.commit()
                    cursor.close()
                    conn.close()

                    if name_delete is not None:
                        space_name = 'tugasakhir'
                        space_file_name_to_delete = name_delete[0]  # Nama file yang ingin dihapus
                        parsed_url = urlparse(space_file_name_to_delete)
                        file_name = os.path.basename(parsed_url.path)
                        print(file_name)
                        
                        # Memanggil fungsi untuk menghapus file dari DigitalOcean Spaces
                        delete_from_digitalocean_space_dts(space_name, file_name)

                    # Delete the data from the database using SQL DELETE statement
                    delete_query = "DELETE FROM spasial_input_user WHERE id_kelas_tutupan_lahan = %s;"
                    cursor.execute(delete_query, (row[0],))
                    conn.commit()
                    st.success("Data deleted successfully!")
                    st.experimental_rerun()  # Rerun the app 

            st.warning (f"Note from admin: {row[9]}")
            # Edit button
            if not st.session_state.get(f"edit_mode_{row[0]}", False):
                if st.button(f"Edit ID {row[0]}"):
                    st.session_state[f"edit_mode_{row[0]}"] = True
                    st.experimental_rerun()  # Rerun the app 
            else:
                new_latitude = st.number_input("New Latitude", value=row[3])
                new_longitude = st.number_input("New Longitude", value=row[4])
                new_location = st.text_input("New Location", value=row[6])
                new_date = st.date_input("New Date", value=row[7])
                

                if st.button(f"Update ID {row[0]}"):
                    # Update the database using SQL UPDATE statement
                    update_query = "UPDATE spasial_input_user SET latitude = %s, longitude = %s, location = %s, date = %s  WHERE id_kelas_tutupan_lahan = %s;"
                    cursor.execute(update_query, (new_latitude, new_longitude, new_location, new_date, row[0]))
                    conn.commit()

                    st.session_state[f"edit_mode_{row[0]}"] = False
                    st.success("Data updated successfully!")
                    st.experimental_rerun()  # Rerun the app 

                if st.button(f"Close ID {row[0]}"):
                    st.session_state[f"edit_mode_{row[0]}"] = False
                    st.experimental_rerun()  # Rerun the app 

        # Close the cursor and connection
        cursor.close()
        conn.close()


