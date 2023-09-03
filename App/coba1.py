import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import psycopg2

# Function to upload file to DigitalOcean Spaces
def upload_to_digitalocean_space(file_data, space_name, space_file_name):
   # Konfigurasi akun DigitalOcean Spaces
    s3 = boto3.client('s3', endpoint_url='https://tugasakhir.sgp1.digitaloceanspaces.com',
                    aws_access_key_id='DO00ATNNKV4K77MB29DB', aws_secret_access_key='WeVAgMDRhl2QWxw2cErT+/hPsgf4JzZNRjEXVF7xqnQ')

    try:
        # Upload the file to the Space in the "data/image" folder
        s3.upload_fileobj(file_data, space_name, f"fotoprofileimage/{space_file_name}")

        print("File berhasil diunggah!")
        return True
    except NoCredentialsError:
        print("Tidak ditemukan kredensial yang valid. Pastikan Anda telah mengatur do_access_key_id dan do_secret_access_key.")
        return False

# Set up Streamlit app
st.title("Update Profile Picture")

# Input for uploading a new profile picture
new_image = st.file_uploader("Upload New Profile Picture", type=["png", "jpg"])

# Update button
if new_image is not None:
    if st.button("Update Profile Picture"):
        # Get the original filename
        original_filename = new_image.name

        # Upload the new image to DigitalOcean Spaces
        space_name = 'tugasakhir'

        if upload_to_digitalocean_space(new_image, space_name, original_filename):
            # Update the image in the database using SQL UPDATE statement
            conn = psycopg2.connect("your_database_connection_string")  # Replace with your actual connection string
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET profile_picture = %s WHERE id = %s", (original_filename, session_state.session_data['user_id_login'],))
            conn.commit()
            cursor.close()
            conn.close()

            # Show a success message
            st.success("Profile picture updated successfully!")



import boto3
from botocore.exceptions import NoCredentialsError

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

# Example usage
space_name = 'tugasakhir'
space_file_name_to_delete = 'user123_uploaded.png'  # Ganti dengan nama file yang ingin dihapus
delete_from_digitalocean_space(space_name, space_file_name_to_delete)
