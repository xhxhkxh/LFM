from flask import Blueprint, request, session, make_response, render_template
from modules import db as db_module
from modules.utils import encode, ph

bp = Blueprint('home', __name__)


@bp.route('/home/m')
def mobile_home():
    return render_template('login-re-m.htm')


@bp.route('/')
def home():
    return render_template('login_remake.htm')
