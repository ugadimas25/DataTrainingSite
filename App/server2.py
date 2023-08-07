# server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import uuid
from Processdataview import process_for_view


app = Flask(__name__)
CORS(app)  # Allow requests from all domains

# Dictionary to store data_ewkb for each user
user_data_ewkb = {}
user_data_startDate = {}
user_data_endDate = {}

# Lock for accessing user_data
data_lock = threading.Lock()

def clear_user_data(user_id):
    # Wait for 6 minutes before clearing the data for the user
    time.sleep(360)

    # Lock the data access to prevent conflicts
    with data_lock:
        if user_id in user_data_ewkb:
            user_data_ewkb.pop(user_id)

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    user_id = data.get('user_id') 
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    struser_id = str(user_id)
   
    print(user_id)

    # Process the data as needed in your Python program
    # Replace this with your actual data processing code
    # response_data = process_for_view(polygon, startDate, endDate)
    response_data = process_for_view(data)

    # Lock the data access to prevent conflicts
    with data_lock:
        user_data_ewkb[struser_id] = response_data
        user_data_startDate[struser_id]= startDate
        user_data_endDate[struser_id]= endDate 

        print(user_data_ewkb[struser_id])
        print(user_data_startDate[struser_id])
        print( user_data_endDate[struser_id])

        # Start a new thread to clear the user data after 6 minutes
        threading.Thread(target=clear_user_data, args=(user_id,)).start()

    return jsonify(response_data)

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    data = request.get_json()
    user_id = data.get('user_id')

    # Lock the data access to prevent conflicts
    with data_lock:
        user_data_resp_ewkb = user_data_ewkb.get(user_id, None)
        user_data_resp_startDate = user_data_startDate.get(user_id, None)
        user_data_resp_endDate = user_data_endDate.get(user_id, None)
        print("gettttttttttttttttttttttttt")
        print(user_data_resp_ewkb,user_data_resp_startDate,user_data_resp_endDate)
        print("Brom..........................................")
        

    return jsonify(user_data_resp_ewkb,user_data_resp_startDate,user_data_resp_endDate)

if __name__ == '__main__':
    app.debug = True  # Enable debug mode
    app.run(port=5002)  # By default, it will run on http://127.0.0.1:5002/
