import serial
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime, timezone

ser = serial.Serial('/dev/serial/by-id/usb-Arm_BBC_micro:bit_CMSIS-DAP_99063602000528205c9da592a8e64dec000000006e052820-if01', 115200)

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

try:
    while True:
        line = ser.readline().decode().strip()

        if line == "on":
            print("Alarm has been turned ON")
            write_to_influxdb("Alarm", "ON")

        elif line == "off":
            print("Alarm has been turned OFF")
            write_to_influxdb("Alarm", "OFF")

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

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
    client.close()