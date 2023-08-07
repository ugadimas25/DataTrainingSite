import streamlit as st
import psycopg2
from PIL import Image
import io
import base64

def create_connection():
        connection = psycopg2.connect(
            host="db.fesgpwzjkedykiwpmatt.supabase.co",
            database="postgres",
            user="postgres",
            password="17agustus2023",
            port='5432'
        )
        return connection

def app():
    st.title("Profile Admin")
     
    with st.container():
        # Create a cursor object to execute queries
        conn = create_connection()
        cursor = conn.cursor()
    
        # Execute a query to retrieve the data
        cursor.execute("SELECT id_kelas_tutupan_lahan, id_users, kelas_tutupan_lahan, latitude, longitude, geom,location,date,image_data, admin_note FROM spasial_input_user")

        # Fetch all the rows returned by the query
        data = cursor.fetchall()

        # Display the data in Streamlit
        for row in data:
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            with col1:
                st.write("ID:", row[0])
            with col2:
                st.write("Latitude:", row[3])
            with col3:
                st.write("Longitude:", row[4])
            with col4:
                # Check for null or empty image value
                if row[8] is not None and len(row[8]) > 0:
                    # Convert bytea to PIL Image
                    image_bytes = io.BytesIO(row[8])
                    image = Image.open(image_bytes)
                    st.image(image, use_column_width=True)
                else:
                    st.write("No image available")

            # Allow the user to upload a new image
            new_image = st.file_uploader(f"Update Image for ID {row[0]}", type=["png", "jpg"])

            if new_image is not None:
                # Read the image data
                image_data = new_image.read()

                # Update the image in the database using SQL UPDATE statement
                id_to_update = row[0]
                cursor.execute("UPDATE location_images SET image_data = %s WHERE id = %s", (psycopg2.Binary(image_data), id_to_update))
                connection.commit()

                # Show a success message
                st.success("Image updated successfully!")

        # Close the cursor and connection
        cursor.close()
        conn.close()



    with st.container():
        st.write("---")
        st.header("Data need to verivy")
        st.write("---")
        # Create a cursor object to execute queries
        conn = create_connection()
        cursor = conn.cursor()

        # Execute a query to retrieve the data
        cursor.execute("SELECT id_kelas_tutupan_lahan, id_users, kelas_tutupan_lahan, latitude, longitude, geom,location,date,image_data, admin_note FROM spasial_input_user")

        # Fetch all the rows returned by the query
        data = cursor.fetchall()

        # Display the data in Streamlit
        main_table_data = []
        for row in data:
            # Generate unique keys for each column based on the 'id' column
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.write(f"ID: {row[0]}")
            col2.write(f"Latitude: {row[3]}")
            col3.write(f"Longitude: {row[4]}")
            # Check for null or empty image value
            if row[8] is not None and len(row[8]) > 0:
                # Convert bytea to PIL Image
                image_bytes = io.BytesIO(row[8])
                image = Image.open(image_bytes)
                col4.image(image, use_column_width=True)
            else:
                col4.write("No image available")

            # If admin, show the "Transfer" button
            transfer_button = col5.button(f"Transfer ID {row[0]}")
            if transfer_button:

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

                # Insert data into the location_images table and remove the row from the rumah table
                cursor.execute("INSERT INTO spasial_data_training_site(id_kelas_tutupan_lahan, id_users, kelas_tutupan_lahan, latitude, longitude, geom,location,date,image_data) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

                cursor.execute("DELETE FROM spasial_input_user WHERE id_kelas_tutupan_lahan = %s", (row[0],))
                conn.commit()

            col6.write(f"Admin Note: {row[9]}")

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Display the data transferred to the main table
        if main_table_data:
            st.write("Data Transferred to Main Table:")
            st.table(main_table_data)


