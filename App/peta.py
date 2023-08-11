import streamlit as st
import streamlit.components.v1 as components
import geopandas as gpd
from App.login import get_session_state
from shapely import wkb
import requests
import json
from App.Generateiduser import get_id_generate, id_call_generator
import psycopg2
import pandas as pd
import io 
from PIL import Image 
#Get draw polygon format ewkb from python server
def get_user_data_from_server(dataid):
 
    # API endpoint URL for getting user_data_ewkb
    api_url = "https://server2.trainingsite.online/get_user_data"

    # Prepare the request data
    data = {"user_id": str(dataid)}
    print("teeeeeeeeeeetttttt")
    print(data)
    try:
        # Make the API call
        response = requests.post(api_url, json=data)
        
        # Check if the response status code indicates success
        if response.status_code == 200:
            # Try parsing the response as JSON
            try:
                user_data_ewkb = response.json()
                st.session_state.user_data_ewkb = user_data_ewkb 
                print("noooooooooooooooooooooooooooooo")
                print(st.session_state.user_data_ewkb)
                print("laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                return user_data_ewkb
            except ValueError:
                # If parsing fails, assume the response is not in JSON format
                return response.content
        else:
            st.error(f"Failed to fetch user data. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # Catch any request-related exceptions
        st.error(f"Failed to fetch user data. Error: {e}")
        return None


# def run_query(query, params=None):
#     try:
#         connection = psycopg2.connect("your_connection_string_here")
#         cursor = connection.cursor()
#         cursor.execute(query, params)
#         result = cursor.fetchall()
#         cursor.close()
#         connection.close()
#         return result
#     except psycopg2.Error as e:
#         print("Error executing query:", e)
#         return None


# To show the result of data view
def view_result():
    
    # Your EWKB data in hexadecimal format
    print("nanassssssssssssssssssssssssssssssssss")
    print (st.session_state.user_data_ewkb)
    ewkb_hex_data = st.session_state.user_data_ewkb[0]
    ewkb_binary_data = bytes.fromhex(ewkb_hex_data)
    startDate = st.session_state.user_data_ewkb[1]
    endDate = st.session_state.user_data_ewkb[2]
    # Establish a connection to the database
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

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Perform the spatial query
    sql_query = """
        SELECT *
        FROM spasial_data_training_site
        WHERE ST_Intersects(geom, ST_SetSRID(%s::geometry, 4326))
    """
    # Execute the spatial query by passing ewkb_binary_data as a parameter
    cursor.execute(sql_query, [psycopg2.Binary(ewkb_binary_data)])



    # Fetch the results
    results = cursor.fetchall()

    # Print the results (you can process them as needed)
    print(results)

        # Display the data in Streamlit
    for row in results:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            st.write("Latitude:", row[3])
        with col2:
            st.write("Longitude:", row[4])
        with col3:
            st.write("Geom:", row[5])
        with col4:
            # Check for null or empty image value
            if row[8] is not None and len(row[8]) > 0:
                # Convert bytea to PIL Image
                image_bytes = io.BytesIO(row[8])
                image = Image.open(image_bytes)
                st.image(image, use_column_width=True)
            else:
                st.write("No image available")


    
    # # Show tabel
    # # Perform the spatial query
    # query_2 = """
    #     SELECT *
    #     FROM spasial_data_training_site
    #     WHERE ST_Intersects(geom, ST_SetSRID(%s::geometry, 4326))
    # """
    # cursor.execute(query_2, [psycopg2.Binary(ewkb_binary_data)])
    # rows = cursor.fetchall()


    # data=pd.DataFrame(rows)
    # data.columns= ['id_kelas_tutupan_lahan', 'id_users', 'kelas_tutupan_lahan', 'latitude', 'longitude', 'geom', 'location', 'date', 'image_data']
    # # Selecting only the desired columns for display
    # selected_columns =  ['kelas_tutupan_lahan', 'latitude', 'longitude', 'date', 'image_data']
    # data_selected = data[selected_columns]

    # # Display the selected columns in the Streamlit table
    # st.table(data_selected)
           
    # Close the cursor and connection
    cursor.close()
    connection.close()



#Display map
def app():

    st.title("map")

    # Initialize session_state and id_user
    session_state = get_session_state()
    id_user= get_id_generate()

    if  id_user.user_id is None:
        id_call_generator()
        
    
    user_id_for_save = id_user.user_id
    print(f"roooooooo {user_id_for_save}")
    print( user_id_for_save)
    # Call the upload_file function
    if not session_state.login and session_state.session_data == None:
        st.error("You must be logged in to upload your file")
    else:
        st.write("If you want to upload data, Go to upload page!")

    # # Render the Leaflet map in Streamlit
    components.html(
    f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Leaflet Draw</title>

        <style>
            html, body, #map {{
                height: 80vh;
                width: 100%;
                margin: 0;
                padding: 0;
            }}
        </style>

    </head>
    <body>

        <label for="startDate">Start Date:</label>
        <input type="date" id="startDate" name="startDate" onchange="'applyFilter()','sendDataToPython()','filterData()'">

        <label for="endDate">End Date:</label>
        <input type="date" id="endDate" name="endDate" onchange="'applyFilter()','sendDataToPython()','filterData()'">



        <div id="map"></div>

        

        <!-- leaflet js  -->
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.2/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.2/dist/leaflet.js"></script>

        <!-- leaflet draw plugin  -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.css"/>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.4.2/leaflet.draw.js"></script>

        <!-- buffer library -->
        <script src="https://cdn.jsdelivr.net/npm/buffer-es6/dist/buffer.js"></script>

        <!-- wkx library -->
        <script src="https://unpkg.com/wkx@0.5.0/dist/wkx.min.js"></script>
        <!-- <script src="wkx.js"></script> -->

        <script>console.log('Your unique user ID is: {user_id_for_save}');</script>

        <script>
             // Function to handle date inputs onchange event
            function applyFilter() {{
                var startDate = document.getElementById("startDate").value;
                var endDate = document.getElementById("endDate").value;
            }}


            // Initialize map with leaflet library
            function initialize() {{
                // Initialize the map
                var map = L.map('map').setView([28.2096, 83.9856], 13);

                // Add the OpenStreetMap tiles
                var osm = L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }});
                osm.addTo(map);

                // Leaflet draw 
                var drawnFeatures = new L.FeatureGroup();
                map.addLayer(drawnFeatures);

                var drawControl = new L.Control.Draw({{
                    edit: {{
                        featureGroup: drawnFeatures,
                        remove: true
                    }},
                    draw: {{
                        polygon: false,
                        polyline: false,
                        rectangle: true,
                        circle: false
                    }}
                }});
                map.addControl(drawControl);
                

                map.on("draw:created", function(e) {{
                    var layer = e.layer;
                    drawnFeatures.addLayer(layer);

                    
                    // Get the values of the start and end date inputs
                    var startDate = document.getElementById("startDate").value;
                    var endDate = document.getElementById("endDate").value;

                    // Send the geoJSONData to the Python server
                    sendDataToPython(layer.toGeoJSON(), startDate, endDate);

                    //send to filterdata
                    filterData(layer.toGeoJSON(), startDate, endDate);     
                }});


                //Assuming you have a function to send an HTTP POST request for send data draw to python server
                function sendDataToPython(data, startDate, endDate) {{
                    // Add user_id to the data
                    data.user_id = "{user_id_for_save}"; // The user_id will be dynamically replaced in the HTML
                    data.startDate = startDate
                    data.endDate = endDate
                    console.log(data.startDate)
                    console.log(data.endDate)

                    fetch("https://server2.trainingsite.online/process_data", {{
                        method: 'POST',
                        headers: {{
                        'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify(data)
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        console.log('Data sent successfully!');
                        console.log(data); // If the Python server sends a response back

                        // Save the data in a hidden element in the DOM
                        // var hiddenElement = document.getElementById('response-data');
                        // hiddenElement.value = JSON.stringify(data);
                        // hiddenElement.dispatchEvent(new Event('change'));

                        // Now you can use the result for further processing or send it to Python for division.
                        // For simplicity, I'll show how to pass the result to Python.

                        // We will need a Python server to handle this data, so we don't lose context between the two languages.
                        // You can use Flask in Python to set up the server for receiving the data from JavaScript.
                    }})
                    .catch(error => console.error('Error sending data to Python:', error));
                }}


                // Assuming you have a function to send an HTTP POST request for send data draw to JS server
                function filterData(polygon, startDate, endDate) {{
                    const polygonJSON = JSON.stringify(polygon);
            
                    const requestData = {{
                        polygon: polygonJSON,
                        startDate: startDate,
                        endDate: endDate
                    }};
                    console.log(startDate)
                    console.log(endDate)

                    fetch('https://server.trainingsite.online/api/data', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify({{ requestData }})
                     }})
                    .then((response) => response.json())
                    .then((data) => {{
                        drawnFeatures.clearLayers();
                        
                        console.log(data)
                        data.forEach(function (point) {{
                            var ewkb = point.geom; // Assuming the EWKB data is provided as "geom" property in the data object
                            console.log(ewkb)
                            var geometry = ewkbToGeometry(ewkb); // Call the function to convert EWKB to Leaflet geometry

                            var marker = L.marker(geometry.getLatLng()).addTo(drawnFeatures);
                            marker.bindPopup(point.name);
                        }});
                    }})
                    .catch((error) => {{
                        console.error('Error retrieving filtered data:', error);
                    }});
                }}

                // function to convert data EWKB to be Geometry
                function ewkbToGeometry(ewkb) {{
                    var wkx = require('wkx');
                    var Buffer = require('buffer').Buffer;

                    var wkbBuffer = new Buffer(ewkb, 'hex');
                    var geometry = wkx.Geometry.parse(wkbBuffer);

                    if ('x' in geometry && 'y' in geometry) {{
                        const lat = geometry.y;
                        const lng = geometry.x;
                        return L.marker([lat, lng]);
                    }}

                    const type = geometry.constructor.name;

                    const latLngs = geometry.toGeoJSON().geometry.coordinates;
                    const leafletLatLngs = latLngs.map(coord => L.latLng(coord[1], coord[0]));

                    let leafletGeometry;

                    if (type === 'LineString' || type === 'LinearRing') {{
                        leafletGeometry = L.polyline(leafletLatLngs);
                    }} else if (type === 'Polygon') {{
                        leafletGeometry = L.polygon(leafletLatLngs);
                    }} else if (type === 'MultiPoint') {{
                        leafletGeometry = L.layerGroup(leafletLatLngs.map(latLng => L.marker(latLng)));
                    }} else if (type === 'MultiLineString') {{
                        leafletGeometry = L.layerGroup(leafletLatLngs.map(latLngs => L.polyline(latLngs)));
                    }} else if (type === 'MultiPolygon') {{
                        leafletGeometry = L.layerGroup(leafletLatLngs.map(latLngs => L.polygon(latLngs)));
                    }}

                    return leafletGeometry;
                }}



            }}

        
        </script>

        <script>
            window.onload = initialize; // Call initialize function when the window loads
        </script>

    </body>
    </html>
      """, height=500)
    
    

    with st.container():
        st.write("---")
                            
       # Display button to fetch user_data_ewkb
        if  id_user.user_id is None:
            print("pretttttttttttttttttttttttt")
            print(id_user.user_id)
            st.error("Please Draw Polygon.")
        else:
            if st.button("Fetch User Data"):
                print("remmmmmmmmmmmmmmmmmmmmmmm")
                print(id_user.user_id)
                # Get user_data_ewkb for the current user
                get_user_data_from_server(id_user.user_id)
                if st.session_state.user_data_ewkb is not None:
                    st.success("User data fetched successfully.")
                else:
                    st.warning("No user data available.")        

        if st.session_state.user_data_ewkb is not None:
            view_result()

        

    

