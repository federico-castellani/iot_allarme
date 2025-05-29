from influxdb_client import InfluxDBClient
import serial
from flask import (Blueprint, render_template, request, jsonify)

# bp definition
bp = Blueprint('Dashboard', __name__, url_prefix='/')

# Connection to influxDB (model)
client = InfluxDBClient(url="http://localhost:8086", token="JXlsndTMgZC-Z8UC-whqGdWezu0SjlyEK9fYLJ-DtQ-_Ud8cx2MTn3c9X8b-6-NouBXXUH08cPeO-tVmcZSdJg==", org="microbit-org")
bucket = "microbit"
query_api = client.query_api()

# Serial port
ser_scrittura = serial.Serial('/dev/serial/by-id/usb-Arm_BBC_micro:bit_CMSIS-DAP_99063602000528205c9da592a8e64dec000000006e052820-if01', 115200, timeout=1)


# Dashboard Route
@bp.route('/')
def dashboard():
    return render_template('Dashboard.html')


# Last alarm status fetch, used to sync the switch on dashboard page load
@bp.route('/get_last_status', methods=['GET'])
def get_last_status():
    try:
        # prepare the query
        query = '''
            from(bucket: "microbit")
              |> range(start: -1d)
              |> filter(fn: (r) => r._measurement == "Alarm" and (r._field == "status") and (r._value == "ON" or r._value == "OFF"))
              |> sort(columns: ["_time"], desc: true)
              |> limit(n:1)
        '''

        # execute the query
        result = query_api.query(org="microbit-org", query=query)

        # recover the last switch status
        if result and result[0].records:
            last_value = result[0].records[0].get_value()
            return jsonify({'status': last_value})
        else:
            return jsonify({'status': 'UNKNOWN'})

    # give out an error
    except Exception as e:
        return jsonify({'status': 'ERROR', 'error': str(e)})


# switch update on click
@bp.route('/update_switch', methods=['POST'])
def update_switch():
    status = request.json.get('status')
    return jsonify({
        'status': 'success',
        'alarmStatus': status
    })


# Serial write route
@bp.route('/execute_write', methods=['POST'])
def execute_write():
    try:
        ser_scrittura.write(b'A')
        ser_scrittura.flush()
        return jsonify({'status': 'success', 'message': 'Command sent'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



