import functools
from datetime import datetime



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('Dashboard', __name__, url_prefix='/')

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

@bp.route('/')
def dashboard():
    return render_template('Dashboard.html', time=current_time)