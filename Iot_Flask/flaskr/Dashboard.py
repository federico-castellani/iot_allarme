import functools
import threading
from datetime import datetime
import subprocess
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('Dashboard', __name__, url_prefix='/')

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

def run_lettura():
    subprocess.run(['python', '-m', 'flaskr.lettura'], check=True)

thread = threading.Thread(target=run_lettura, daemon=True)
thread.start()


@bp.route('/')
def dashboard():
    return render_template('Dashboard.html', time=current_time)

@bp.route('/execute_scrittura', methods=['POST'])
def execute_scrittura():
    try:
        subprocess.run(['python', 'flaskr/scrittura.py'], check=True)
        return jsonify({'status': 'success', 'message': 'scrittura.py executed successfully'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/update_switch', methods=['POST'])
def update_switch():
    status = request.json.get('status')
    return jsonify({
        'status': 'success',
        'alarmStatus': status
    })
