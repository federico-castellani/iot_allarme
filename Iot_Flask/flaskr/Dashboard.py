import functools
from datetime import datetime
import subprocess
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

bp = Blueprint('Dashboard', __name__, url_prefix='/')

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

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