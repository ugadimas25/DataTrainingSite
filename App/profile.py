import streamlit as st
import psycopg2
from PIL import Image
import io
from App.login import get_session_state

def create_connection():
        connection = psycopg2.connect(
            # host="db.fesgpwzjkedykiwpmatt.supabase.co",
            # database="postgres",
            # user="postgres",
            # password="17agustus2023",
            # port='5432'
            host="170.64.133.197",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

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
            image_data BYTEA,
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
        selected_option = st.selectbox('Select an option', ['No', 'Update Profile'])

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

            

        
        new_image = st.file_uploader(f"Update Profile Picture", type=["png", "jpg"])

        if new_image is not None:
            # Read the image data
            # Allow the user to upload a new image
            image_data = new_image.read()

            # Update the image in the database using SQL UPDATE statement
           
            cursor.execute("UPDATE users SET profile_picture = %s WHERE  id = %s", (psycopg2.Binary(image_data), session_state.session_data['user_id_login'],))
            conn.commit()

            # Show a success message
            st.success("Image updated successfully!")
     
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
                # Read the image data
                image_data = new_image.read()

                # Update the image in the database using SQL UPDATE statement
                id_to_update = row[0]
                cursor.execute("UPDATE spasial_input_user SET image_data = %s WHERE id_kelas_tutupan_lahan = %s", (psycopg2.Binary(image_data), id_to_update))
                conn.commit()

                # Show a success message
                st.success("Image updated successfully!")
               

                

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
                    image_bytes = io.BytesIO(row[8])
                    image = Image.open(image_bytes)
                    st.image(image, use_column_width=True)
                else:
                    st.write("No image available")
            
            with col6:
                # Delete button
                if st.button(f"Delete ID {row[0]}"):
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


