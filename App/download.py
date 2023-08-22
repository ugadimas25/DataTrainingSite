import streamlit as st
import psycopg2
import base64
import pandas as pd
from io import BytesIO
import zipfile
from App.login import get_session_state
import geopandas as gpd
from shapely.wkb import loads
import tempfile
import os
from shapely import wkb
import geopandas as gpd
import zipfile
import os
from zipfile import ZipFile
import shutil


def create_connection():
        connection = psycopg2.connect(
            # host="db.fesgpwzjkedykiwpmatt.supabase.co",
            # database="postgres",
            # user="postgres",
            # password="17agustus2023",
            # port='5432',

            host="170.64.133.197",
            database="postgres",
            user="postgres",
            password="admin",
            port='5432'
        )
        return connection

def Download_Excel():
    ewkb_hex_data = st.session_state.user_data_ewkb[0]
    ewkb_binary_data = bytes.fromhex(ewkb_hex_data)
    startDate = st.session_state.user_data_ewkb[1]
    endDate = st.session_state.user_data_ewkb[2]

    conn = create_connection()
    cursor = conn.cursor()

    # Perform the spatial query
    sql_query = """
        SELECT *
        FROM spasial_data_training_site
        WHERE ST_Intersects(geom, ST_GeomFromEWKB(%s))
        AND date BETWEEN %s AND %s
    """
    # Execute the spatial query by passing ewkb_binary_data as a parameter
    cursor.execute(sql_query, [psycopg2.Binary(ewkb_binary_data), startDate, endDate])

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    df = pd.DataFrame(results)  # Convert the results to a DataFrame

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data.xlsx">Download Excel file</a>'
    st.markdown(href, unsafe_allow_html=True)



def Download_CSV():
    ewkb_hex_data = st.session_state.user_data_ewkb[0]
    ewkb_binary_data = bytes.fromhex(ewkb_hex_data)
    startDate = st.session_state.user_data_ewkb[1]
    endDate = st.session_state.user_data_ewkb[2]

    conn = create_connection()
    cursor = conn.cursor()

    # Perform the spatial query
    sql_query = """
        SELECT *
        FROM spasial_data_training_site
        WHERE ST_Intersects(geom, ST_GeomFromEWKB(%s))
        AND date BETWEEN %s AND %s
    """
    # Execute the spatial query by passing ewkb_binary_data as a parameter
    cursor.execute(sql_query, [psycopg2.Binary(ewkb_binary_data), startDate, endDate])

    results = cursor.fetchall()

    cursor.close()
    conn.close()
    
    df = pd.DataFrame(results)  # Convert the results to a DataFrame

    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="download.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)



def Download_Shapefile():
    ewkb_hex_data = st.session_state.user_data_ewkb[0]
    ewkb_binary_data = bytes.fromhex(ewkb_hex_data)
    startDate = st.session_state.user_data_ewkb[1]
    endDate = st.session_state.user_data_ewkb[2]

    conn = create_connection()
    cursor = conn.cursor()

    # Perform the spatial query
    sql_query = """
        SELECT *
        FROM spasial_data_training_site
        WHERE ST_Intersects(geom, ST_GeomFromEWKB(%s))
        AND date BETWEEN %s AND %s
    """

    cursor.execute(sql_query, [psycopg2.Binary(ewkb_binary_data), startDate, endDate])

    results = cursor.fetchall()

    cursor.close()
    conn.close()
    print(results)
    jumlah_data = len(results)
    print("Jumlah baris data:", jumlah_data)
    
    geometries = []  # Initialize the list to store geometries
    
    for row in results:
        geometry_data = row[5]  # Change to the appropriate index for geometry column
        geometry = wkb.loads(bytes.fromhex(geometry_data))
        geometries.append(geometry)
    
    # Create GeoDataFrame from geometry objects
    gdf = gpd.GeoDataFrame({'geometry': geometries})
    
    # Display the GeoDataFrame as a table
    st.write("GeoDataFrame:")
    st.write(gdf)

  
    # Create a temporary directory to store Shapefile components
    temp_dir = tempfile.mkdtemp()
    shapefile_path = os.path.join(temp_dir, 'shapefile')
    os.makedirs(shapefile_path)

    # Save the GeoDataFrame as a Shapefile
    gdf.to_file(shapefile_path, driver='ESRI Shapefile')

    # Create a ZipFile containing the Shapefile components
    zip_file_path = os.path.join(temp_dir, 'shapefile.zip')
    with ZipFile(zip_file_path, 'w') as zipf:
        for file_name in os.listdir(shapefile_path):
            file_path = os.path.join(shapefile_path, file_name)
            zipf.write(file_path, os.path.basename(file_path))

    # Offer the user a downloadable link for the Zip file
    with open(zip_file_path, 'rb') as zip_file:
        b64 = base64.b64encode(zip_file.read()).decode()
        href = f'<a href="data:application/zip;base64,{b64}" download="shapefile.zip">Download Shapefile</a>'
        st.markdown(href, unsafe_allow_html=True)

    # Clean up temporary files
    shutil.rmtree(temp_dir)