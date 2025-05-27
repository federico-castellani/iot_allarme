from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi

import serial
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('Dashboard', __name__, url_prefix='/')

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

client = InfluxDBClient(url="http://localhost:8086", token="JXlsndTMgZC-Z8UC-whqGdWezu0SjlyEK9fYLJ-DtQ-_Ud8cx2MTn3c9X8b-6-NouBXXUH08cPeO-tVmcZSdJg==", org="microbit-org")
bucket = "microbit"
query_api = client.query_api()

@bp.route('/')
def dashboard():
    return render_template('Dashboard.html', time=current_time)

ser_scrittura = serial.Serial('/dev/serial/by-id/usb-Arm_BBC_micro:bit_CMSIS-DAP_990536020005283324da877ee04823fa000000006e052820-if01', 115200, timeout=1)

@bp.route('/execute_scrittura', methods=['POST'])
def execute_scrittura():
    try:
        ser_scrittura.write(b'A')
        ser_scrittura.flush()
        return jsonify({'status': 'success', 'message': 'Command sent'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/update_switch', methods=['POST'])
def update_switch():
    status = request.json.get('status')
    return jsonify({
        'status': 'success',
        'alarmStatus': status
    })


@bp.route('/get_last_status', methods=['GET'])
def get_last_status():
    try:
        query = f'''
            from(bucket:"microbit")
              |> range(start: -1h)
              |> filter(fn: (r) => r._measurement == "Alarm")
              |> sort(columns: ["_time"], desc: true)
              |> limit(n:1)
        '''
        result = query_api.query(org="microbit-org", query=query)

        if result and result[0].records:
            last_value = result[0].records[0].get_value()
            return jsonify({'status': last_value})
        else:
            return jsonify({'status': 'UNKNOWN'})
    except Exception as e:
        return jsonify({'status': 'ERROR', 'error': str(e)})
