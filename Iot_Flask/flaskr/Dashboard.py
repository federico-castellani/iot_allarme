import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


bp = Blueprint('Dashboard', __name__, url_prefix='/')

@bp.route('/')
def dashboard():
    return render_template('Dashboard.html')