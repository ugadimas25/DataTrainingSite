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
        query = "SELECT profile_picture FROM users WHERE id = %s;"
        cursor.execute(query, (session_state.session_data['user_id_login'],))
        check_image_profile = cursor.fetchall()

        
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
                cursor.execute("UPDATE spasial_input_user SET image_data = %s WHERE id_kelas_tutupan_lahan = %s", (psycopg2.Binary(image_data), id_to_update))
                conn.commit()

                # Show a success message
                st.success("Image updated successfully!")

        # Close the cursor and connection
        cursor.close()
        conn.close()


