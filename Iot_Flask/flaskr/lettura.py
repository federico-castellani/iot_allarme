import serial
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

ser = serial.Serial('/dev/ttyACM1', 115200)

client = InfluxDBClient(url="http://localhost:8086", token="JXlsndTMgZC-Z8UC-whqGdWezu0SjlyEK9fYLJ-DtQ-_Ud8cx2MTn3c9X8b-6-NouBXXUH08cPeO-tVmcZSdJg==", org="microbit-org")
bucket = "microbit"

def write_to_influxdb(dataType, data):
    timestamp = datetime.now(timezone.utc)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    try:
        point = (
            Point(dataType)  
            .field("status", str(data)) 
            .time(timestamp, WritePrecision.NS)
        )
        write_api.write(bucket=bucket, record=point)
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

def update_dashboard(status):
    try:
        response = requests.post('http://localhost:5000/update_switch',
                               json={'status': status})
        if response.status_code != 200:
            print(f"Failed to update dashboard: {response.text}")
    except Exception as e:
        print(f"Error updating dashboard: {e}")


try:
    while True:
        try:
            line = ser.readline().decode().strip()


            if line == "on":
                print("Alarm has been turned ON")
                write_to_influxdb("Alarm", "ON")
                update_dashboard("ON")


            elif line == "off":
                print("Alarm has been turned OFF")
                write_to_influxdb("Alarm", "OFF")
                update_dashboard("OFF")


            elif line == "s":
                print("Alarm has been SILENCED")
                write_to_influxdb("Alarm", "SILENCED")

            elif line == "m":
                print("Movement detected")
                write_to_influxdb("Movement", "DETECTED")

            elif line == "A":
                print("OK")

            else:
                print("Unknown data received:", line)
            ser.reset_input_buffer()

        except Exception as e:
            print(f"Error reading serial data: {e}")

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
    client.close()