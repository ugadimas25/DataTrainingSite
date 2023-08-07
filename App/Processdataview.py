# data_processing.py
from shapely import wkb
from shapely.geometry import shape
import binascii
import psycopg2

ewkb_data = None

def get_variable_ewkb():
    global ewkb_data
    print("variable ewkb")
    print(ewkb_data)
    
    return ewkb_data


def process_for_view(data):
    global ewkb_data  # Declare ewkb_data as a global variable
    # Process the data as needed in your Python program
    # For example, you can access the features using data['features']
    # and perform further processing or analysis
    print("Processing data...")
    geojson_data = data

    # Convert GeoJSON to Shapely geometry
    shapely_geometry = shape(geojson_data['geometry'])

    # Convert Shapely geometry to WKB (Well-Known Binary) format
    wkb_data = shapely_geometry.wkb

    # Convert bytes to hexadecimal string
    wkb_hex = wkb_data.hex()

    # Convert Shapely geometry to EWKB (Extended Well-Known Binary) format
    ewkb_data = wkb.dumps(shapely_geometry, srid=4326, hex=True)


    print(wkb_hex)
    print(ewkb_data)

    return ewkb_data


