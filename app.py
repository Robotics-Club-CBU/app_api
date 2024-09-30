import os
import time
import pandas as pd
from flask import Flask, request, jsonify
from influxdb_client_3 import InfluxDBClient3, Point

app = Flask(__name__)

# InfluxDB configuration
token = ' '
org = "staginh"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "robotics-bucket"
ssl_verify = False

client = InfluxDBClient3(host=host, token=token, org=org, ssl_verify=ssl_verify)

@app.route('/write', methods=['POST'])
def write_data():
    data = request.json
    point = (
        Point("car_metrics")
        .tag("vehicle", data["vehicle"])
        .field("temperature", data["temperature"])
        .field("battery_percentage", data["battery_percentage"])
        .field("lights_on", data["lights_on"])
        .field("indicator_left_on", data["indicator_left_on"])
        .field("indicator_right_on", data["indicator_right_on"])
    )
    client.write(database=database, record=point)
    return jsonify({"message": "Car data written to InfluxDB"}), 200

@app.route('/read', methods=['GET'])
def read_data():
    query = """SELECT *
               FROM 'car_metrics'
               WHERE time >= now() - interval '24 hours'
               AND (temperature IS NOT NULL 
                    OR battery_percentage IS NOT NULL 
                    OR lights_on IS NOT NULL 
                    OR indicator_left_on IS NOT NULL 
                    OR indicator_right_on IS NOT NULL)"""
    try:
        # Execute the query
        table = client.query(query=query, database=database, language='sql')
        
        # Convert to DataFrame
        df = table.to_pandas().sort_values(by="time")
        
        # Convert DataFrame to JSON
        data = df.to_dict(orient='records')
        
        return jsonify(data), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
